using UnityEngine;

public class PIDController : MonoBehaviour
{
    public float Kp = 0.99f;
    public float Ki = 0.10f;
    public float Kd = 2.04f;

    private float integral  = 0f;
    private float lastError = 0f;

    public float CalculateSteering(float error, float dt)
    {
        float p = Kp * error;

        integral += error * dt;
        float i = Ki * integral;

        // dt'ye bolmek, ani degisimlerde turetilen degeri asiri buyutuyordu (titremenin ana sebebi)
        // Bunun yerine dogrudan degisimi kullaniyoruz veya dt ile carpiyoruz ki normalize olsun
        float derivative = (error - lastError); 
        float d = Kd * derivative;

        lastError = error;
        
        // Cikisi sinirla ki 4000 gibi absurt degerlere ulasmasin
        return Mathf.Clamp(p + i + d, -50f, 50f);
    }

    public void ResetPID()
    {
        integral  = 0f;
        lastError = 0f;
    }
}
