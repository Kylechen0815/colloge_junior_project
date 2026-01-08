using UnityEngine;

public class CameraSwitcher : MonoBehaviour
{
    public Camera mainCamera;         // 主視角
    public Camera characterCamera;    // 角色視角
    public Camera topDownCamera;      // 俯視相機

    public GameObject player;         // 玩家（你會手動拖）
    public GameObject ball;           // 球（你會手動拖）

    public GameObject playerMarker;   // 玩家標示（可手動拖，未填則自動建立）
    public GameObject ballMarker;     // 球標示（可手動拖，未填則自動建立）

    public SocketReceiver socketeceiver; // 控制切換的腳本

    private Camera[] cameras;
    private int currentIndex = 0;

    void Start()
    {
        // ✅ 如果沒有設定 playerMarker，則自動生成
        if (playerMarker == null && player != null)
        {
            playerMarker = GameObject.CreatePrimitive(PrimitiveType.Sphere);
            playerMarker.transform.SetParent(player.transform);
            playerMarker.transform.localScale = new Vector3(4f, 4f, 4f);
            playerMarker.transform.localPosition = new Vector3(0, 2f, 0);
            playerMarker.GetComponent<Renderer>().material.color = Color.red;
            Destroy(playerMarker.GetComponent<Collider>());
        }

        // ✅ 如果沒有設定 ballMarker，則自動生成
        if (ballMarker == null && ball != null)
        {
            ballMarker = GameObject.CreatePrimitive(PrimitiveType.Sphere);
            ballMarker.transform.SetParent(ball.transform);
            ballMarker.transform.localScale = new Vector3(20f, 20f,20f);
            ballMarker.transform.localPosition = new Vector3(0, 1.2f, 0);
            ballMarker.GetComponent<Renderer>().material.color = Color.yellow;
            Destroy(ballMarker.GetComponent<Collider>());
        }

        cameras = new Camera[] { mainCamera, characterCamera, topDownCamera };

        for (int i = 0; i < cameras.Length; i++)
            cameras[i].enabled = (i == currentIndex);

        UpdateMarkers(); // 初始狀態更新
    }

    void Update()
    {
        if (socketeceiver != null && socketeceiver.canchangecam)
        {
            SwitchCamera();
            // socketeceiver.canchangecam = false;
        }
    }

    public void SwitchCamera()
    {
        cameras[currentIndex].enabled = false;

        currentIndex = (currentIndex + 1) % cameras.Length;

        cameras[currentIndex].enabled = true;

        UpdateMarkers();

        Debug.Log($"📷 已切換到相機：{cameras[currentIndex].name}");
    }

    private void UpdateMarkers()
    {
        bool isTopDown = cameras[currentIndex] == topDownCamera;

        if (playerMarker != null)
            playerMarker.SetActive(isTopDown);

        if (ballMarker != null)
            ballMarker.SetActive(isTopDown);
    }
}
