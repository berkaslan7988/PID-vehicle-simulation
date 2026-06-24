using UnityEngine;
using System.Text;
using System.IO;
using System.Linq;

[ExecuteInEditMode]
public class TrackTracer : MonoBehaviour
{
    void OnEnable()
    {
        var sb = new StringBuilder();
        sb.AppendLine("=== MANUEL WAYPOINT POZISYONLARI ===");
        
        // Sahnedeki tum "Yol" iceren objeleri bul
        var allObjects = FindObjectsByType<Transform>(FindObjectsSortMode.None);
        var yolObjects = allObjects
            .Where(t => t.name.StartsWith("Yol"))
            .OrderBy(t => {
                // "Yol" -> 0, "Yol (1)" -> 1, "Yol (2)" -> 2, ...
                string name = t.name;
                if (name == "Yol") return 0;
                // "Yol (X)" -> X
                int start = name.IndexOf('(');
                int end = name.IndexOf(')');
                if (start >= 0 && end > start)
                {
                    string numStr = name.Substring(start + 1, end - start - 1).Trim();
                    if (int.TryParse(numStr, out int num)) return num;
                }
                return 999;
            })
            .ToArray();
        
        sb.AppendLine($"Toplam {yolObjects.Length} adet Yol objesi bulundu:\n");
        
        for (int i = 0; i < yolObjects.Length; i++)
        {
            var t = yolObjects[i];
            var pos = t.position;
            sb.AppendLine($"{i}: \"{t.name}\" -> X:{pos.x:F1} Y:{pos.y:F1} Z:{pos.z:F1}");
        }
        
        // Araba pozisyonunu da kaydet
        var car = GameObject.Find("Fortina");
        if (car != null)
        {
            sb.AppendLine($"\nARABA: X:{car.transform.position.x:F1} Y:{car.transform.position.y:F1} Z:{car.transform.position.z:F1}");
        }
        
        // TrackGenerator objesinin pozisyonu
        var tg = GameObject.Find("TrackGenerator");
        if (tg != null)
        {
            sb.AppendLine($"TRACK_GEN: X:{tg.transform.position.x:F1} Y:{tg.transform.position.y:F1} Z:{tg.transform.position.z:F1}");
        }
        
        string path = Application.dataPath + "/ManualWaypoints.txt";
        File.WriteAllText(path, sb.ToString());
        Debug.Log("[TrackTracer] Manuel waypoint pozisyonlari yazildi: " + path);
    }
}
