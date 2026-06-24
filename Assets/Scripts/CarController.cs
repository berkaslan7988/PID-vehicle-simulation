using UnityEngine;
using System.IO;
using System.Collections.Generic;
using System.Globalization;

public class CarController : MonoBehaviour
{
    public float speed = 15f; // Hiz biraz artirildi

    [HideInInspector] public Transform[] waypoints;
    [HideInInspector] public int loopStartIndex = 0;

    public float CurrentError  { get; private set; }
    public float CurrentOutput { get; private set; }
    public bool  IsFinished    { get; private set; }

    private PIDController pid;
    private Rigidbody     rb;
    private int           waypointIndex = 0;

    // CSV Kayit Sistemi
    private struct PIDRecord
    {
        public float time;
        public float error;
        public float output;
        public float speed;
    }
    private List<PIDRecord> records = new List<PIDRecord>();
    private float startTime;

    void Start()
    {
        pid = GetComponent<PIDController>();
        rb  = GetComponent<Rigidbody>();
        
        // Fizik ayarlarini sifirla, saf fizik kullanacagiz
        rb.constraints = RigidbodyConstraints.FreezeRotationX | RigidbodyConstraints.FreezeRotationZ;
        rb.useGravity = true;
        rb.isKinematic = false;

        startTime = Time.time;
        records.Clear();
    }

    public float lookaheadDistance = 4f;

    void FixedUpdate()
    {
        if (waypoints == null || waypoints.Length == 0) return;

        // 1. Arabaya en yakin waypoint'i bul
        int bestIndex = waypointIndex;
        float minDist = float.MaxValue;
        
        for (int i = -5; i < 15; i++)
        {
            int idx = (waypointIndex + i + waypoints.Length) % waypoints.Length;
            float dist = Vector3.Distance(transform.position, waypoints[idx].position);
            if (dist < minDist)
            {
                minDist = dist;
                bestIndex = idx;
            }
        }
        waypointIndex = bestIndex;

        // Dinamik Bakis Mesafesi (Dynamic Lookahead)
        // Araba hizliysa daha uzaga bakar (sallanmayi/serit degistirmeyi onler)
        // Araba yavasladiginda daha yakina bakar (virajlari iceriden kesmeyi onler)
        float currentSpeed = rb.linearVelocity.magnitude;
        float actualLookahead = Mathf.Clamp(currentSpeed * 0.7f, 6f, 18f);
        
        float accumulatedDist = 0f;
        int targetIndex = bestIndex;
        Vector3 exactTargetPos = waypoints[bestIndex].position;
        
        while (accumulatedDist < actualLookahead)
        {
            int nextIdx = (targetIndex + 1) % waypoints.Length;
            float segLen = Vector3.Distance(waypoints[targetIndex].position, waypoints[nextIdx].position);
            
            if (accumulatedDist + segLen >= actualLookahead) 
            {
                // Istenilen mesafeye ulasildi, bu segment uzerinde interpolate et
                float t = (actualLookahead - accumulatedDist) / Mathf.Max(segLen, 0.001f);
                exactTargetPos = Vector3.Lerp(waypoints[targetIndex].position, waypoints[nextIdx].position, t);
                break;
            }
            
            accumulatedDist += segLen;
            targetIndex = nextIdx;
            
            if (targetIndex == bestIndex) break; 
        }

        // PID HATASI: Hedef acisi (Yumusatilmis sanal hedef noktasi kullaniliyor)
        Vector3 localTarget = transform.InverseTransformPoint(exactTargetPos);
        float error = Mathf.Atan2(localTarget.x, Mathf.Max(localTarget.z, 0.1f)) * Mathf.Rad2Deg;

        float output = pid.CalculateSteering(error, Time.fixedDeltaTime);
        
        CurrentError  = error;
        CurrentOutput = output;

        // CSV'ye kaydet
        records.Add(new PIDRecord
        {
            time = Time.time - startTime,
            error = error,
            output = output,
            speed = rb.linearVelocity.magnitude
        });

        // Ileri hareket (Virajlarda otomatik yavaslama)
        float targetSpeed = speed;
        if (Mathf.Abs(error) > 5f) 
        {
            // Freni cok daha kistim: Hizi virajin keskinligine gore daha az dusuruyor (120'ye boluyoruz)
            float speedFactor = Mathf.Clamp01(1f - (Mathf.Abs(error) / 120f));
            // Minimum hizi 14 m/s (yaklasik 50 km/h) yaptik, momentumu koruyacak.
            targetSpeed = Mathf.Max(14f, speed * speedFactor);
        }

        // Hizi aninda degistirmek yerine ivmelenme/frenleme ile yumusat
        float currentFwdSpeed = Vector3.Dot(rb.linearVelocity, transform.forward);
        float newFwdSpeed = Mathf.Lerp(currentFwdSpeed, targetSpeed, Time.fixedDeltaTime * 5f);

        Vector3 fwd = transform.forward * newFwdSpeed;
        rb.linearVelocity = new Vector3(fwd.x, rb.linearVelocity.y, fwd.z);

        // Dönüş
        float turnRate = output * 3.0f;
        rb.MoveRotation(rb.rotation * Quaternion.Euler(Vector3.up * turnRate * Time.fixedDeltaTime));
    }

    void OnApplicationQuit()
    {
        SaveCSV();
    }

    void OnDisable()
    {
        SaveCSV();
    }

    private bool csvSaved = false;

    void SaveCSV()
    {
        if (csvSaved || records.Count == 0) return;
        csvSaved = true;

        string filePath = Path.Combine(Application.dataPath, "..", "pid_verileri.csv");
        filePath = Path.GetFullPath(filePath);

        using (StreamWriter writer = new StreamWriter(filePath, false, System.Text.Encoding.UTF8))
        {
            // Baslik satiri
            writer.WriteLine("Zaman(s);Hata_e(t);Cikis_u(t);Hiz(m/s)");

            foreach (var r in records)
            {
                writer.WriteLine(string.Format(CultureInfo.InvariantCulture, 
                    "{0:F4};{1:F4};{2:F4};{3:F4}", 
                    r.time, r.error, r.output, r.speed));
            }
        }

        Debug.Log($"[CSV] {records.Count} satir kaydedildi: {filePath}");
    }
}
