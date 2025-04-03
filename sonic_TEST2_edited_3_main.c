
/* USER CODE BEGIN PD */
#define ECHO_Pin GPIO_PIN_0
#define ECHO_GPIO_Port GPIOA
#define TRIG_Pin GPIO_PIN_5
#define TRIG_GPIO_Port GPIOA
#define PB0_Pin GPIO_PIN_0
#define PB0_GPIO_Port GPIOB
/* USER CODE END PD */

/* USER CODE BEGIN PV */
uint32_t IC_Val1 = 0; // 發射時間點
uint32_t IC_Val2 = 0; // 接收時間點
uint32_t Difference = 0;  // 發射接收時間差 ( IC_Val2 - IC_Val1 )
uint8_t Is_First_Captured = 0;  //標記訊號上升下降狀態
float Distance = 0.0;         // 物距 ( 時差Difference * 聲速 )

/* USER CODE END PV */

/* USER CODE BEGIN PFP */

void delay_us(uint16_t TRIGGER_t) {  //因為函式庫內 delay() 單位為毫秒ms，因此需自定義微秒延遲器
    __HAL_TIM_SET_COUNTER(&htim3, 0);  // 設定計數器歸零
    while (__HAL_TIM_GET_COUNTER(&htim3) < TRIGGER_t ); // while持續進行直到計數器 = TRIGGER_t
}

// 發送 Trig 信號 ( 長度為10微渺的高電位 )
void HCSR04_Trigger() {
    HAL_GPIO_WritePin(TRIG_GPIO_Port, TRIG_Pin, GPIO_PIN_SET);  // 高電位
    delay_us(10);  // 保持 10us
    HAL_GPIO_WritePin(TRIG_GPIO_Port, TRIG_Pin, GPIO_PIN_RESET);  // 低電位
}

// 接收 Echo 信號
void HAL_TIM_IC_CaptureCallback(TIM_HandleTypeDef *htim) {
	if (htim->Instance == TIM2 && htim->Channel == HAL_TIM_ACTIVE_CHANNEL_1){
        if (Is_First_Captured == 0) {  // 第一次捕獲上升沿
        	// 這次中斷是 TIM2_CH1 觸發的，執行距離計算
            IC_Val1 = HAL_TIM_ReadCapturedValue(htim, TIM_CHANNEL_1);
            Is_First_Captured = 1;
            __HAL_TIM_SET_CAPTUREPOLARITY(htim, TIM_CHANNEL_1, TIM_INPUTCHANNELPOLARITY_FALLING);
        } else {  // 第二次捕獲下降沿
            IC_Val2 = HAL_TIM_ReadCapturedValue(htim, TIM_CHANNEL_1);
            Difference = IC_Val2 - IC_Val1;
            Distance = (Difference * 0.0343) / 2;
            Is_First_Captured = 0;
            __HAL_TIM_SET_CAPTUREPOLARITY(htim, TIM_CHANNEL_1, TIM_INPUTCHANNELPOLARITY_RISING);
        }
    }
}

/* USER CODE END PFP */

  /* USER CODE BEGIN 2 */
  HAL_TIM_IC_Start_IT(&htim2, TIM_CHANNEL_1);
  HAL_TIM_Base_Start(&htim3);

  /* USER CODE END 2 */

  /* USER CODE BEGIN WHILE */
  while (1)
  {	 HCSR04_Trigger();
  	  HAL_Delay(100);
  	  printf("Distance: %.2f cm\r\n", Distance);
  	if (Distance > 0 && Distance < 50) {  // 設定範圍，小於50cm
  	    HAL_GPIO_WritePin(GPIOB, GPIO_PIN_0, GPIO_PIN_SET);
  	} else {
  	    HAL_GPIO_WritePin(GPIOB, GPIO_PIN_0, GPIO_PIN_RESET);
  	}

    /* USER CODE END WHILE */

    /* USER CODE BEGIN 3 */
  }
  /* USER CODE END 3 */
}
