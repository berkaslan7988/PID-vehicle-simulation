using UnityEngine;

/// <summary>
/// Play modunda sahneyi raycast ile tarar ve köprü/rampa yüzeyini bulur.
/// Sonuçları Console'a ve dosyaya yazar. Sonra silinebilir.
/// </summary>
public class BridgeFinder : MonoBehaviour
{
    void Start()
    {
        var sb = new System.Text.StringBuilder();
        sb.AppendLine("=== BRIDGE FINDER - Raycast Sonuclari ===");
        
        // Kirmizi daire bolgesini tara (X=350-650, Z=-250 to -100)
        sb.AppendLine("\n--- KOPRU BOLGESI (X:350-650, Z:-250 to -100) ---");
        for (float x = 350f; x <= 650f; x += 20f)
        {
            for (float z = -260f; z <= -80f; z += 20f)
            {
                RaycastHit hit;
                if (Physics.Raycast(new Vector3(x, 50f, z), Vector3.down, out hit, 100f))
                {
                    if (hit.point.y > 3f)
                    {
                        sb.AppendLine("X:" + x.ToString("F0") + " Z:" + z.ToString("F0") + 
                                      " Y:" + hit.point.y.ToString("F1") + 
                                      " obj:" + hit.collider.gameObject.name);
                    }
                }
            }
        }
        
        // Arabanin suanki konumundan koprüye dogru bir line ciz
        sb.AppendLine("\n--- RAMPA HATTI (250,-100) -> (600,-220) ---");
        for (float t = 0f; t <= 1f; t += 0.02f)
        {
            float x = Mathf.Lerp(250f, 650f, t);
            float z = Mathf.Lerp(-100f, -230f, t);
            RaycastHit hit;
            if (Physics.Raycast(new Vector3(x, 50f, z), Vector3.down, out hit, 100f))
            {
                sb.AppendLine("t:" + t.ToString("F2") + " X:" + x.ToString("F0") + 
                              " Z:" + z.ToString("F0") + " Y:" + hit.point.y.ToString("F1") +
                              " obj:" + hit.collider.gameObject.name);
            }
        }

        // Dogu tarafindaki potansiyel rampa
        sb.AppendLine("\n--- DOGU RAMPASI (X:400-600, Z=-200 sabit hat) ---");
        for (float x = 250f; x <= 700f; x += 15f)
        {
            RaycastHit hit;
            if (Physics.Raycast(new Vector3(x, 50f, -200f), Vector3.down, out hit, 100f))
            {
                sb.AppendLine("X:" + x.ToString("F0") + " Y:" + hit.point.y.ToString("F1") +
                              " obj:" + hit.collider.gameObject.name);
            }
        }
        
        // Alternatif: Z=-180 hattı
        sb.AppendLine("\n--- Z=-180 HATTI ---");
        for (float x = 250f; x <= 700f; x += 15f)
        {
            RaycastHit hit;
            if (Physics.Raycast(new Vector3(x, 50f, -180f), Vector3.down, out hit, 100f))
            {
                sb.AppendLine("X:" + x.ToString("F0") + " Y:" + hit.point.y.ToString("F1") +
                              " obj:" + hit.collider.gameObject.name);
            }
        }

        // Alternatif: Z=-160 hattı
        sb.AppendLine("\n--- Z=-160 HATTI ---");
        for (float x = 250f; x <= 700f; x += 15f)
        {
            RaycastHit hit;
            if (Physics.Raycast(new Vector3(x, 50f, -160f), Vector3.down, out hit, 100f))
            {
                sb.AppendLine("X:" + x.ToString("F0") + " Y:" + hit.point.y.ToString("F1") +
                              " obj:" + hit.collider.gameObject.name);
            }
        }

        string result = sb.ToString();
        Debug.Log(result);
        
        string path = Application.dataPath + "/BridgeFinderResults.txt";
        System.IO.File.WriteAllText(path, result);
        Debug.Log("[BridgeFinder] Sonuclar yazildi: " + path);
    }
}
