using UnityEngine;

public class MyUIManager : MonoBehaviour
{
    public CarController car;
    public PIDController pid;
    public Rigidbody     carRb;

    private const int GW      = 280;
    private const int GH      = 80;
    private const int HISTORY = GW;

    private float[] errorHistory  = new float[HISTORY];
    private float[] outputHistory = new float[HISTORY];
    private int     histHead      = 0;

    private Texture2D errorTex;
    private Texture2D outputTex;

    private float maxError  = 10f;
    private float maxOutput = 5f;

    void Start()
    {
        if (car   == null) car   = FindObjectOfType<CarController>();
        if (pid   == null) pid   = FindObjectOfType<PIDController>();
        if (carRb == null && car != null) carRb = car.GetComponent<Rigidbody>();

        errorTex  = MakeTex(GW, GH, new Color(0.08f, 0.08f, 0.12f));
        outputTex = MakeTex(GW, GH, new Color(0.08f, 0.08f, 0.12f));
    }

    void Update()
    {
        if (car == null) return;

        errorHistory [histHead % HISTORY] = car.CurrentError;
        outputHistory[histHead % HISTORY] = car.CurrentOutput;
        histHead++;

        float ae = Mathf.Abs(car.CurrentError);
        float au = Mathf.Abs(car.CurrentOutput);
        if (ae * 1.2f > maxError)  maxError  = ae * 1.2f;
        if (au * 1.2f > maxOutput) maxOutput = au * 1.2f;

        DrawGraph(errorTex,  errorHistory,  histHead, maxError,  new Color(0.2f, 1f, 0.4f));
        DrawGraph(outputTex, outputHistory, histHead, maxOutput, new Color(1f, 0.6f, 0.1f));
    }

    void OnGUI()
    {
        if (car == null || pid == null) return;

        // Kucuk boyutlu sol panel
        float panelW = 170f;
        float panelH = 280f;
        float px     = 6f;
        float py     = 6f;

        GUI.color = new Color(0f, 0f, 0f, 0.7f);
        GUI.DrawTexture(new Rect(px, py, panelW, panelH), Texture2D.whiteTexture);
        GUI.color = Color.white;

        GUIStyle small = new GUIStyle(GUI.skin.label);
        small.fontSize = 10;
        small.normal.textColor = new Color(0.9f, 0.9f, 0.95f);

        GUIStyle header = new GUIStyle(GUI.skin.label);
        header.fontSize = 10;
        header.fontStyle = FontStyle.Bold;
        header.normal.textColor = new Color(0.5f, 0.8f, 1f);

        float y = py + 4f;
        float sliderW = panelW - 16f;

        GUI.Label(new Rect(px + 4, y, sliderW, 16), "PID PARAMETRELER", header); y += 16;

        GUI.Label(new Rect(px + 4, y, sliderW, 14), "Kp = " + pid.Kp.ToString("F2"), small); y += 14;
        pid.Kp = GUI.HorizontalSlider(new Rect(px + 4, y, sliderW, 12), pid.Kp, 0f, 5f); y += 16;

        GUI.Label(new Rect(px + 4, y, sliderW, 14), "Ki = " + pid.Ki.ToString("F2"), small); y += 14;
        pid.Ki = GUI.HorizontalSlider(new Rect(px + 4, y, sliderW, 12), pid.Ki, 0f, 1f); y += 16;

        GUI.Label(new Rect(px + 4, y, sliderW, 14), "Kd = " + pid.Kd.ToString("F2"), small); y += 14;
        pid.Kd = GUI.HorizontalSlider(new Rect(px + 4, y, sliderW, 12), pid.Kd, 0f, 2f); y += 20;

        GUI.Label(new Rect(px + 4, y, sliderW, 16), "ARAC", header); y += 16;

        GUI.Label(new Rect(px + 4, y, sliderW, 14), "Hiz = " + car.speed.ToString("F1") + " m/s", small); y += 14;
        car.speed = GUI.HorizontalSlider(new Rect(px + 4, y, sliderW, 12), car.speed, 2f, 20f); y += 16;

        if (carRb != null)
        {
            GUI.Label(new Rect(px + 4, y, sliderW, 14), "Kutle = " + carRb.mass.ToString("F0") + " kg", small); y += 14;
            carRb.mass = GUI.HorizontalSlider(new Rect(px + 4, y, sliderW, 12), carRb.mass, 500f, 3000f); y += 18;
        }

        // Anlik degerler
        GUIStyle val = new GUIStyle(small);
        val.normal.textColor = new Color(0.3f, 1f, 0.5f);
        GUI.Label(new Rect(px + 4, y, sliderW, 14), "e(t) = " + car.CurrentError.ToString("F2") + " deg", val); y += 14;
        val.normal.textColor = new Color(1f, 0.7f, 0.2f);
        GUI.Label(new Rect(px + 4, y, sliderW, 14), "u(t) = " + car.CurrentOutput.ToString("F2"), val);

        // Grafik paneli (sag ust kose)
        float gx = px + panelW + 6f;
        float gy = py;
        float graphPanelW = GW + 12f;
        float graphPanelH = GH * 2 + 38f;

        GUI.color = new Color(0f, 0f, 0f, 0.7f);
        GUI.DrawTexture(new Rect(gx, gy, graphPanelW, graphPanelH), Texture2D.whiteTexture);
        GUI.color = Color.white;

        GUI.Label(new Rect(gx + 4, gy + 2, GW, 14), "e(t) [derece]", header);
        if (errorTex  != null) GUI.DrawTexture(new Rect(gx + 4, gy + 16, GW, GH), errorTex);

        GUI.Label(new Rect(gx + 4, gy + GH + 20, GW, 14), "u(t)", header);
        if (outputTex != null) GUI.DrawTexture(new Rect(gx + 4, gy + GH + 34, GW, GH), outputTex);
    }

    void DrawGraph(Texture2D tex, float[] history, int head, float scale, Color lineCol)
    {
        Color bg = new Color(0.08f, 0.08f, 0.12f);
        Color[] pixels = new Color[GW * GH];
        for (int i = 0; i < pixels.Length; i++) pixels[i] = bg;
        tex.SetPixels(pixels);

        Color grid = new Color(0.2f, 0.2f, 0.28f);
        int midY = GH / 2;
        for (int x = 0; x < GW; x++)
            tex.SetPixel(x, midY, grid);

        for (int i = 1; i < HISTORY; i++)
        {
            int idx0 = (head - HISTORY + i - 1 + HISTORY * 2) % HISTORY;
            int idx1 = (head - HISTORY + i     + HISTORY * 2) % HISTORY;

            float v0 = history[idx0];
            float v1 = history[idx1];
            if (scale < 0.001f) scale = 0.001f;

            int y0 = Mathf.Clamp(midY + Mathf.RoundToInt(v0 / scale * (midY - 2)), 0, GH - 1);
            int y1 = Mathf.Clamp(midY + Mathf.RoundToInt(v1 / scale * (midY - 2)), 0, GH - 1);

            int yMin = Mathf.Min(y0, y1);
            int yMax = Mathf.Max(y0, y1);
            for (int py = yMin; py <= yMax; py++)
                tex.SetPixel(i, py, lineCol);
        }

        Color zero = new Color(0.4f, 0.4f, 0.5f);
        for (int x = 0; x < GW; x++) tex.SetPixel(x, midY, zero);
        tex.Apply();
    }

    static Texture2D MakeTex(int w, int h, Color col)
    {
        var t = new Texture2D(w, h);
        Color[] px = new Color[w * h];
        for (int i = 0; i < px.Length; i++) px[i] = col;
        t.SetPixels(px);
        t.Apply();
        return t;
    }
}
