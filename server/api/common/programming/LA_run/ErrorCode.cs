﻿using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Runtime.InteropServices;

namespace C_Sharp
{
	class LA_ErrorCode
	{
		public enum ErrorCode
		{
			 LA_SDK_ERR_OK						= 0,
			//Success, No Error!!//
			//沒有錯誤//

			 LA_SDK_ERR_LA_NOT_INITIAL			= 0x001,
			//Need to call ulaSDKInit() to initiate LA before calling other funciton//
			//使用SDK前請先初始化LA//

			 LA_SDK_ERR_TRIGINFO				= 0x010,
			//Sample Rate Can't be 0//
			//採樣率不能為0//

			 LA_SDK_ERR_TOO_MANY_TRIG_CONDITION	= 0x011,
			//Too many Trigger condition, max level is 16					//
			//Decrease to 8 if rising edge / falling edge condition used	//
			//Decrease to 4 if Change edge condition used					//
			//觸發條件超出最大設定量，最大為16階，有使用上升或下降緣時最大值會下降為8階//
			//使用變化緣時最大值會下降為4階//

			 LA_SDK_ERR_CH_NUM_OUT_OF_RANGE		= 0x012,
			//Input Ch number is out of range//
			//設定超出允許通道數//

			 LA_SDK_ERR_TRIGSET_CANNOT_BUILD	= 0x013,
			//Trig set build error, builded trig set over max level //
			//Clear the trig set and reduce the trig condition		//
			//觸發參數組產生失敗，產生出來的組合超出觸發階層最大上限//
			//請重新產生新的觸發參數並減少部分觸發條件				//

			 LA_SDK_ERR_INPUT_BAD_POINTER		= 0x014,
			//Input pointer variable is a bad pointer//
			//傳入參數為bad pointer//

			 LA_SDK_ERR_INPUT_INVALID_CONDITION	= 0x015,
			//Input Trig condition is invalid, reference the following table//
			//觸發條件設定錯誤，觸發條件需為下列數值//
			//LA_TRIG_DONT_CARE, LA_TRIG_LOW, LA_TRIG_HIGH, LA_TRIG_RISING, LA_TRIG_FALLING, LA_TRIG_CHANGE//

			 LA_SDK_ERR_DEVICE_NOT_SUPPORT		= 0x016,
			//Current device is not support the Rising / Falling /Either Edge condition//
			//該機種不支援上升/下降/交替變化緣觸發//

			 LA_SDK_ERR_GET_LA_DATA_ERR			= 0x017,
			//Request data from LA failed, check the USB connection//
			//從LA取得資料時發生錯誤，可能原因為usb連線中斷//

			 LA_SDK_ERR_SAMPLE_NUM_OUT_OF_RANGE	= 0x018,
			//Specified Sample Number is out of range//
			//設定的取樣點數超出範圍//

			 LA_SDK_ERR_HW_MODE_OUT_OF_RANGE	= 0x019,
			//Specified HW Mode is out of range//
			//指定硬體參數範圍超出設定//

			 LA_SDK_ERR_INPUT_VAR_IS_NULL		= 0x020,
			//Input Variable(Pointer) is NULL//
			//傳入的指標參數為NULL//

			 LA_SDK_ERR_VAR_NOT_READY			= 0x021,	
			//Need to call ulaSDKCaputre() to get datas before ulaSDKSaveAsLawFile()//
			//呼叫 ulaSDKSaveAsLawFile() 前應先呼叫 ulaSDKCaputre() 才能取得當前的參數與數據//

			 LA_SDK_ERR_FILE_OPEN_FAIL			= 0x022,
			//Save File Create Error, target dir is Protected or insufficient disk space//
			//儲存檔案失敗，目標位置無法開啟或是受到保護//

			 LA_SDK_ERR_STATUS_GET_ERROR		= 0x023,
			//Cannot get La Current HW mode //
			//無法取得目前LA的硬體狀態//

			 LA_SDK_ERR_FILE_FORMAT_ERROR		= 0x024,
			//Target file format unknown//
			//不支援指定的檔案格式//

			 LA_SDK_ERR_FILE_READ_FAIL			= 0x025,
			//LAW file read error, file does not exist or is protected//
			//無法開啟Law檔，檔案不存在或是受到保護//

			 LA_SDK_ERR_OLD_VERSION				= 0x026,
			//Specified a higher version LAW file, please contact Acute for new SDK version//
			//目標檔案為較新版本之LAW檔，請聯絡Acute以取得更新版SDK軟體//

			 LA_SDK_ERR_BUFFER_TOO_SMALL		= 0x027,
			//Buffer size too small(<= 0)//
			//輸入BufferSize過小(可能小於等於0)//

			 LA_SDK_ERR_FW_TOO_OLD				= 0x028,
			//Firmware too old, please contact Acute//
			//韌體功能過舊, 請聯絡Acute工程師//

			 LA_SDK_ERR_DELAYTRIG_OUT_OF_RANGE	= 0x029,
			//Delay Trigger is limited from 0 to = 0xffffff clocks, please check the input value//
			//延遲觸發最小為0, 最大不得超過= 0xffffff個clock//

			 LA_SDK_ERR_CAPTURE_IN_PROGRESS		= 0x030,
			//The LA is still in capture operation//
			//LA目前仍在擷取中//

			 LA_SDK_ERR_CAPTURE_START_FAILED	= 0x031,
			//Unable to initiate the LA capture operation//
			//LA擷取工作啟動失敗//

			 LA_SDK_ERR_PROCDURE_START_FAILED	= 0x032,
			//Unable to start a new procedure//
			//工作程序啟動失敗//

			 LA_SDK_ERR_TRAN_MODE_DATA			= 0x033,
			//Can not apply Conventional data read function to Transitional data//
			//無法使用一般資料讀取模式讀取轉態儲存資料//

			 LA_SDK_ERR_CONV_MODE_DATA			= 0x034,
			//Can not apply Transitional data read function to Conventional data//
			//無法使用一般資料讀取模式讀取轉態儲存資料//

			 LA_SDK_ERR_HW_FILTER_RANGE_ERR		= 0x035,
			//The specified H/W filter value out of range, maximum value = 35ns//
			//H/W Filter設定超出範圍, 最大值為35ns//
 
			 LA_SDK_ERR_TEMPLATE_FORMAT_ERROR	= 0x036,
			//The specified template file is not a valid .law file or the content was corrupted//
			//讀取保存檔案所使用的樣本波形檔時發生錯誤//

			 LA_SDK_ERR_TRIG_FORMAT_CONV_ERROR	= 0x998,
			//Internal Trigger format convert error, contact Acute//
			//觸發格式轉換發生不明錯誤，請聯絡Acute工程師//

			 LA_SDK_ERR_MEMORY_ACCESS_ERROR		= 0x999,
			//Internal memory copy error, contact Acute//
			//程式內部發生不明錯誤，請聯絡Acute工程師//


		};
	}
}

