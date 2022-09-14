using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Runtime.InteropServices;
using DWORD = System.UInt32;

namespace C_Sharp
{
    public class LARunClass
    {
        // Import the LARun .DLL
		[DllImport("LASDK.dll", EntryPoint = "ulaSDKInit")]
		private static extern bool _ulaSDKInit();
		[DllImport("LASDK.dll", EntryPoint = "ulaSDKShutdown")]
		private static extern bool _ulaSDKShutdown();
		[DllImport("LASDK.dll", EntryPoint = "ulaSDKThreshold")]
		private static extern bool _ulaSDKThreshold(int iPod, int iMiniVolt);
		[DllImport("LASDK.dll", EntryPoint = "ulaSDKGetLaID")]
		private static extern int _ulaSDKGetLaID();
		[DllImport("LASDK.dll", EntryPoint = "ulaSDKIsCaptureReady")]
		private static extern bool _ulaSDKIsCaptureReady();
		[DllImport("LASDK.dll", EntryPoint = "ulaSDKIsTriggerReady")]
		private static extern bool _ulaSDKIsTriggerReady();
		[DllImport("LASDK.dll", EntryPoint = "ulaSDKClearTrigger")]
		private static extern bool _ulaSDKClearTrigger(ref TRIG lptr);
		[DllImport("LASDK.dll", EntryPoint = "ulaSDKSetChTrigger")]
		private static extern bool _ulaSDKSetChTrigger(ref TRIG lptr, int iLevel, int iCh, int iTrig, int iCondLogic);
		[DllImport("LASDK.dll", EntryPoint = "ulaSDKCapture")]
		private static extern bool _ulaSDKCapture(ref TRIG lptr);
		[DllImport("LASDK.dll", EntryPoint = "ulaSDKStopCapture")]
		private static extern bool _ulaSDKStopCapture();
		[DllImport("LASDK.dll", EntryPoint = "ulaSDKGetBusData")]
		private static extern bool _ulaSDKGetBusData(int iMSB, int iLSB, UInt32[] pUserData, ref int lpiSize, int iStartSamplePos);
		[DllImport("LASDK.dll", EntryPoint = "ulaSDKGetChData")]
		private static extern bool _ulaSDKGetChData(int iCh, UInt32[] pUserData, ref int lpiSize, int iStartSamplePos);
		[DllImport("LASDK.dll", EntryPoint = "ulaSDKSetHwInfo")]
		private static extern bool _ulaSDKSetHwInfo(int iIndex, ref int iValue);
        [DllImport("LASDK.dll", EntryPoint = "ulaSDKGetMaxSamplesNum")]
        private static extern int _ulaSDKGetMaxSamplesNum();
        [DllImport("LASDK.dll", EntryPoint = "ulaSDKGetSamplesNum")]
        private static extern int _ulaSDKGetSamplesNum();
        [DllImport("LASDK.dll", EntryPoint = "ulaSDKSetSamplesNum")]
        private static extern bool _ulaSDKSetSamplesNum(int iSize);
        [DllImport("LASDK.dll", EntryPoint = "ulaSDKGetBufferSizeInBytes")]
        private static extern int _ulaSDKGetBufferSizeInBytes();
		[DllImport("LASDK.dll", EntryPoint = "ulaSDKGetLastError")]
		private static extern int _ulaSDKGetLastError();

		[DllImport("LASDK.dll", EntryPoint = "ulaSDKSaveAsLawFile")]
		private static extern bool _ulaSDKSaveAsLawFile(byte[] szFilePathName);
		[DllImport("LASDK.dll", EntryPoint = "ulaSDKSaveAsLawFileWithTemplate")]
		private static extern bool _ulaSDKSaveAsLawFileWithTemplate(byte[] szFilePathName, byte[] szFileTemplateName);

		[DllImport("LASDK.dll", EntryPoint = "ulaSDKSetChannelMask")]
		private static extern bool _ulaSDKSetChannelMask(byte[] i8ChMask, int iSize);
		[DllImport("LASDK.dll", EntryPoint = "ulaSDKSetHwFilter")]
		private static extern bool _ulaSDKSetHwFilter(Int64 i64ChOnOff, int iFilterTime_ns);
		
		[DllImport("LASDK.dll", EntryPoint = "ulaSDKGetTransStoreInfo")]
		private static extern bool _ulaSDKGetTransStoreInfo(ref Int64 i64TrHead, ref Int64 i64TrPos);
		[DllImport("LASDK.dll", EntryPoint = "ulaSDKGetTrWfm")]
		private static extern Int64 _ulaSDKGetTrWfm(Int64 i64Index, byte[] lpb);

        public const int TL_MAX_CH_SIZE = 36;

        public const int TR_CONTINUE = 0;
        public const int TR_DISCONTINUE = 1;
        public const int TR_END = 2;

        public const int LA_TRIG_LOW = 0;
		public const int LA_TRIG_FALLING = 2;
		public const int LA_TRIG_RISING = 4;
        public const int LA_TRIG_HIGH = 6;		
        public const int LA_TRIG_DONT_CARE = 8;
		public const int LA_TRIG_CHANGE = 10;

        public const int TR_ONELEVEL = 0;
        public const int TR_MULTILEVEL = 1;
        public const int TR_DUALCOND = 2;

		public enum LA_HW_SETTING
		{
			SET_TL_MODE = 5,
			SET_TL_QUALIFICATION = 7,
			SET_TL_GLITCH_FILTER = 8,
		};

		public enum LA_HW_MODE
		{
			HW_4G_36CH = 0,
			HW_4G_18CH = 1,
			HW_4G_9CH = 2,
			HW_4G_4CH = 3,
			HW_2G_36CH = 100,
			HW_1600M_4CH = 200,
			HW_800M_9CH = 300,
			HW_400M_18CH = 400,
			HW_200M_36CH = 500,
			HW_200M_18CH = 501,
			HW_200M_12CH = 502,
			HW_200M_9CH = 503,
			HW_200M_6CH = 504,
			HW_200M_4CH = 505,
			HW_200M_2CH = 506,
			HW_200M_1CH = 507,
			HW_200M_32CH_TR = 510,
			HW_200M_8CH_TR = 511,
			HW_EXT_35CH = 600,
			HW_EXT_18CH = 601,
			HW_EXT_12CH = 602,
			HW_EXT_9CH = 603,
			HW_EXT_6CH = 604,
			HW_EXT_4CH = 605,
			HW_EXT_2CH = 606,
			HW_EXT_1CH = 607,
		};

        // _TRIG:iFlag
		public const int TR_DBLMODE = 0x00000001;  // LA work in double freq. mode
		public const int TR_PRETRIG = 0x00000002; // LA work in Pre-trig. mode
      
        
        [StructLayout(LayoutKind.Sequential)]
        public struct TRIG
        {
			public int		iFlag;          // Flag of trigger condition
			public int		iDelay;         // delay trigger setting(unit: clocks)
			public int		iWidth;         // pulse width trigger settings(unit: Clocks)
			public int		iPassCount;     // pass count of trigger condition
			public uint		iFreq;          // LA current sampling rate
			public int		iFreqHi;		// LA current sampling rate (High 32 Bit)
			public int		iExtClk;		// use external clock(if iExtClk = 1: use internal clock)
			public int		iTrPos;			// trigger position
			[MarshalAsAttribute(UnmanagedType.ByValArray, SizeConst = 16)]
			public int[]	lpiCont;       // the trigger condition is running? length is iLvl(unit:int)
			[MarshalAsAttribute(UnmanagedType.ByValArray, SizeConst = 1024)]
			public byte[]	lpbTrigData;   // Trigger data, length = iCh*iLvl (unit: byte)
        }

        [StructLayout(LayoutKind.Sequential)]
        public struct HW_INFO{
            public UInt16 wID; 
            public string pName;
        };

        public static readonly HW_INFO[] m_InfoLst = new HW_INFO[] 
        { 
            new HW_INFO() { wID = 0x2036, pName = "TL2036" },
            new HW_INFO() { wID = 0x2136, pName = "TL2136" },
            new HW_INFO() { wID = 0x2236, pName = "TL2236" },
			new HW_INFO() { wID = 0x2836, pName = "TL2036E" },
			new HW_INFO() { wID = 0x2c36, pName = "TL2136B" },
			new HW_INFO() { wID = 0x2d36, pName = "TL2236B" },
			new HW_INFO() { wID = 0x2e36, pName = "TL2236B+" },
			new HW_INFO() { wID = 0x2018, pName = "TL2018E" },
			new HW_INFO() { wID = 0x2118, pName = "TL2118E" },
            new HW_INFO() { wID = 0x1032, pName = "LA1032" },
            new HW_INFO() { wID = 0x2032, pName = "LA2032" },
            new HW_INFO() { wID = 0x2132, pName = "LA2132" },
            new HW_INFO() { wID = 0x2164, pName = "LA2164" },
            new HW_INFO() { wID = 0x1116, pName = "PKLA1116" },
            new HW_INFO() { wID = 0x1216, pName = "PKLA1216" },
            new HW_INFO() { wID = 0x1616, pName = "PKLA1616" },
            new HW_INFO() { wID = 0, pName = "" },
        };



		public bool ulaSDKInit()
        {
			return _ulaSDKInit();
        }
		public bool ulaSDKShutdown()
        {
			return _ulaSDKShutdown();
        }
		public bool ulaSDKThreshold(int iPod, int iMiniVolt)
        {
			return _ulaSDKThreshold(iPod, iMiniVolt);
        }
		public int ulaSDKGetLaID()
		{
			return _ulaSDKGetLaID();
		}
		public bool ulaSDKIsCaptureReady()
		{
			return _ulaSDKIsCaptureReady();
		}
		public bool ulaSDKIsTriggerReady()
		{
			return _ulaSDKIsTriggerReady();
		}
		public bool ulaSDKSetChTrigger(ref TRIG lptr, int iLevel, int iCh, int iTrig, int iCondLogic)
        {
			return _ulaSDKSetChTrigger(ref lptr, iLevel, iCh, iTrig, iCondLogic);
        }
		public bool ulaSDKClearTrigger(ref TRIG lptr)
		{
			return _ulaSDKClearTrigger(ref lptr);
		}
		public bool ulaSDKCapture(ref TRIG lptr)
        {
            return _ulaSDKCapture(ref lptr);
        }
		public bool ulaSDKGetBusData(int iMSB, int iLSB, UInt32[] pUserData, int lpiSize, int iStartSamplePos)
        {
			return _ulaSDKGetBusData(iMSB, iLSB, pUserData, ref lpiSize, iStartSamplePos);
        }
		public bool ulaSDKGetChData(int iCh, UInt32[] pUserData, int lpiSize, int iStartSamplePos)
		{
			return _ulaSDKGetChData(iCh, pUserData, ref lpiSize, iStartSamplePos);
		}
		public bool ulaSDKSetHwInfo(int iIndex, int iValue)
		{
			return _ulaSDKSetHwInfo(iIndex, ref iValue);
		}
        public int ulaSDKGetMaxSamplesNum()
        {
            return _ulaSDKGetMaxSamplesNum();
        }
        public int ulaSDKGetSamplesNum()
        {
            return _ulaSDKGetSamplesNum();
        }
        public bool ulaSDKSetSamplesNum(int iSize)
        {
            return _ulaSDKSetSamplesNum(iSize);
        }        
        public int ulaSDKGetBufferSizeInBytes()
        {
            return _ulaSDKGetBufferSizeInBytes();
        }
		public int ulaSDKGetLastError()
		{
			return _ulaSDKGetLastError();
		}
		public bool ulaSDKSaveAsLawFile(string strFilePathName)
		{
			byte[] szPathName = System.Text.Encoding.ASCII.GetBytes(strFilePathName + "\0");
			return _ulaSDKSaveAsLawFile(szPathName);
		}
		public bool ulaSDKSaveAsLawFileWithTemplate(string strFilePathName, string strFileTemplate)
		{
			byte[] szPathName = System.Text.Encoding.ASCII.GetBytes(strFilePathName + "\0");
			byte[] szTemplateName = System.Text.Encoding.ASCII.GetBytes(strFileTemplate + "\0");
			return _ulaSDKSaveAsLawFileWithTemplate(szPathName, szTemplateName);
		}
		public bool ulaSDKSetChannelMask(byte[] i8ChMask, int iSize)
		{
			return _ulaSDKSetChannelMask(i8ChMask, iSize);
		}
		public bool ulaSDKSetHwFilter(Int64 i64ChOnOff, int iFilterTime_ns)
		{
			return _ulaSDKSetHwFilter(i64ChOnOff, iFilterTime_ns);
		}

		public bool ulaSDKGetTransStoreInfo(ref Int64 i64TrHead, ref Int64 i64TrPos)
		{
			return _ulaSDKGetTransStoreInfo(ref i64TrHead, ref i64TrPos);
		}
		public Int64 ulaSDKGetTrWfm(Int64 i64Index, byte[] lpb)
		{
			return _ulaSDKGetTrWfm(i64Index, lpb);
		}
		public bool ulaSDKStopCapture()
		{
			return _ulaSDKStopCapture();
		}
    }

}


