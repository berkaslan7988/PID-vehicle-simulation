using UnityEngine;
using System.Collections.Generic;
using System.Linq;

public class TrackGenerator : MonoBehaviour
{
    public CarController carController;
    public float startLateralOffset = 0f;

    private List<Vector3> smoothTrack = new List<Vector3>();
    private Vector3[] dynamicWaypoints = new Vector3[0];

    void Awake()
    {
        FixCityColliders();

        if (carController == null) return;

        // Sahnedeki Yol objelerini dinamik olarak bul
        dynamicWaypoints = GetSceneWaypoints();

        if (dynamicWaypoints.Length >= 2)
        {
            GenerateSmoothTrack(dynamicWaypoints);

            var waypoints = new Transform[smoothTrack.Count];
            for (int i = 0; i < smoothTrack.Count; i++)
            {
                var go = new GameObject("WP_" + i);
                go.transform.SetParent(transform);
                go.transform.position = smoothTrack[i];
                waypoints[i] = go.transform;
            }

            carController.waypoints = waypoints;
            carController.loopStartIndex = 0;

            Vector3 startPos   = smoothTrack[0];
            Vector3 nextPos    = smoothTrack[1];
            Vector3 forwardDir = (nextPos - startPos).normalized;

            Vector3 spawnPos = startPos;
            // Arabayi tam yol yuzeyine yerlestir
            if (Physics.Raycast(new Vector3(startPos.x, startPos.y + 2f, startPos.z), Vector3.down, out RaycastHit hit, 10f))
            {
                spawnPos.y = hit.point.y + 0.1f;
            }
            
            carController.transform.position = spawnPos;
            carController.transform.rotation = Quaternion.LookRotation(forwardDir, Vector3.up);
        }
    }

    Vector3[] GetSceneWaypoints()
    {
        var allTransforms = FindObjectsByType<Transform>(FindObjectsInactive.Include, FindObjectsSortMode.None);
        var yolObjects = allTransforms
            .Where(t => t.name.StartsWith("Yol") && t.GetComponent<TrackGenerator>() == null)
            .OrderBy(t => {
                string name = t.name;
                if (name == "Yol") return 0;
                string numStr = name.Replace("Yol", "").Replace("(", "").Replace(")", "").Trim();
                if (int.TryParse(numStr, out int num)) return num;
                return 999;
            })
            .ToArray();

        if (yolObjects.Length < 2) return new Vector3[0];
        
        Vector3[] points = new Vector3[yolObjects.Length];
        for (int i = 0; i < yolObjects.Length; i++)
        {
            points[i] = yolObjects[i].position;
        }
        return points;
    }

    void FixCityColliders()
    {
        var cityObj = GameObject.Find("demo_city_by_versatile_studio");
        if (cityObj != null)
        {
            var renderers = cityObj.GetComponentsInChildren<MeshRenderer>(true);
            foreach (var r in renderers)
            {
                if (r.gameObject.GetComponent<Collider>() == null)
                {
                    r.gameObject.AddComponent<MeshCollider>();
                }
            }
        }
    }

    void GenerateSmoothTrack(Vector3[] controlPoints)
    {
        if (smoothTrack == null) smoothTrack = new List<Vector3>();
        smoothTrack.Clear();
        
        int numPoints = controlPoints.Length;
        if (numPoints < 2) return;

        // 1. Polyline uzerinde esit aralikli noktalar olustur (Resampling)
        float spacing = 1.0f; // 1 metre aralikla noktalar
        List<Vector3> resampled = new List<Vector3>();
        resampled.Add(controlPoints[0]);

        for (int i = 0; i < numPoints - 1; i++)
        {
            Vector3 start = controlPoints[i];
            Vector3 end = controlPoints[i + 1];
            float dist = Vector3.Distance(start, end);
            int steps = Mathf.Max(1, Mathf.RoundToInt(dist / spacing));
            
            for (int j = 1; j <= steps; j++)
            {
                resampled.Add(Vector3.Lerp(start, end, j / (float)steps));
            }
        }

        // 2. Laplacian Smoothing (Noktalari komsulariyla ortalama)
        int smoothIterations = 80; 
        List<Vector3> smoothed = new List<Vector3>(resampled);
        Vector3[] temp = new Vector3[resampled.Count];

        for (int iter = 0; iter < smoothIterations; iter++)
        {
            temp[0] = smoothed[0]; // Ilk ve son noktalar sabit
            temp[smoothed.Count - 1] = smoothed[smoothed.Count - 1];

            for (int i = 1; i < smoothed.Count - 1; i++)
            {
                temp[i] = (smoothed[i - 1] + smoothed[i] + smoothed[i + 1]) / 3f;
            }
            
            for (int i = 0; i < smoothed.Count; i++) smoothed[i] = temp[i];
        }

        // 3. Y eksenini (yukseklik) yola raycast ile yapistir
        foreach (var p in smoothed)
        {
            Vector3 pos = p;
            if (Physics.Raycast(new Vector3(pos.x, 50f, pos.z), Vector3.down, out RaycastHit hit, 100f))
            {
                pos.y = hit.point.y + 0.5f;
            }
            smoothTrack.Add(pos);
        }
    }

    void OnDrawGizmos()
    {
        // Editorde sahnede Yol objeleri degistikce mavi rotayi dinamik guncelle
        if (!Application.isPlaying) 
        {
            dynamicWaypoints = GetSceneWaypoints();
            if (dynamicWaypoints.Length >= 2)
            {
                GenerateSmoothTrack(dynamicWaypoints);
            }
        }

        if (smoothTrack != null && smoothTrack.Count > 0)
        {
            Gizmos.color = Color.cyan;
            for (int i = 0; i < smoothTrack.Count; i++)
            {
                Gizmos.DrawSphere(smoothTrack[i], 2f);
                if (i < smoothTrack.Count - 1)
                    Gizmos.DrawLine(smoothTrack[i], smoothTrack[i + 1]);
            }
        }
        
        Gizmos.color = Color.red;
        if (dynamicWaypoints != null)
        {
            for (int i = 0; i < dynamicWaypoints.Length; i++)
            {
                Gizmos.DrawSphere(dynamicWaypoints[i], 4f);
            }
        }
    }
}
