using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.ComponentModel;
using System.Data;
using System.Diagnostics;
using System.Timers;
using System.Threading;
using System.IO;
using System.Text;

namespace C_Sharp
{
    public class Program
    {
        LARunClass m_LARun;
        int m_id, m_iCurSize;
        UInt32[] m_lpiWave;
        string csModelName;
        string csErrorString;
        string homeworkPath;
        string PGVName;
        string HWName;
        string homeworkPathLaw;
        string sequential;
        bool getWaveData = false;
        bool gfTrMode;
        LARunClass.LA_HW_MODE m_giHwMode;
        LARunClass.TRIG m_tr = new LARunClass.TRIG();

        System.Threading.Timer MainTimerClock;
        //System.Timers.Timer MainTimerClock;

        private void GetHW()
        {
            int i;

            if (m_LARun.ulaSDKInit())
            {
                m_LARun.ulaSDKThreshold(0, 1600);           // 1.6V (TTL)
                m_LARun.ulaSDKThreshold(1, 1600);           // 1.6V (TTL)
                                                            //因為用的是TL2136B 所以只設定 0 1
                                                            //	m_LARun.ulaSDKThreshold(2, 1600);			// 1.6V (TTL)
                                                            //	m_LARun.ulaSDKThreshold(3, 1600);			// 1.6V (TTL)

                m_id = m_LARun.ulaSDKGetLaID();

                for (i = 0; LARunClass.m_InfoLst[i].wID != 0; i++)
                {
                    if (LARunClass.m_InfoLst[i].wID == m_id)
                        break;
                }

                if (LARunClass.m_InfoLst[i].wID != 0)
                    csModelName = string.Format("{0}: HW Mode = {1}", LARunClass.m_InfoLst[i].pName, m_giHwMode.ToString());
                else
                    csModelName = "Unknown";

                Console.WriteLine(csModelName);

                Console.WriteLine("H/W Initialized");
            }
            else
            {
                ShowErrorCode();
            }
        }

        private void SetTrigger()
        {
            int iTrigContinue;
            int iTrigCondition;
            int iTrigChannel = 0;
            int iTrigLevel = 0;

            if (sequential == "0")
            {
                Console.WriteLine("Combinational Circuit!");
                iTrigContinue = LARunClass.TR_END;
                iTrigCondition = LARunClass.LA_TRIG_CHANGE;
            }
            else
            {
                Console.WriteLine("Sequential Circuit!");
                iTrigContinue = LARunClass.TR_CONTINUE;
                iTrigCondition = LARunClass.LA_TRIG_FALLING;
            }
            //int iTrigContinue = LARunClass.TR_CONTINUE;  //TR_NEXT 0x00 兩觸發條件必須連續達成，中間不可以有其他不同訊號
            //int iTrigContinue = LARunClass.TR_END;      // TR_TRIGGER 0x02 觸發條件已全部設定完畢，啟動觸發
            if (!m_LARun.ulaSDKClearTrigger(ref m_tr))  //clear the trigger setting to free run
            {
                ShowErrorCode();
                return;
            }
            if (!m_LARun.ulaSDKSetChTrigger(ref m_tr, iTrigLevel, iTrigChannel, iTrigCondition, iTrigContinue)) //set trigger for level 0
            {
                ShowErrorCode();
                return;
            }
            //if (!m_LARun.ulaSDKSetChTrigger(ref m_tr, iTrigLevel2, iTrigChannel2, iTrigCondition2, iTrigContinue2))	//set trigger for level 1 if need
            //{
            //    ShowErrorCode();
            //    return;
            //}
        }

        private void LACapture()
        {


            //Set trigger condition to single level trigger
            SetTrigger();
            Console.WriteLine("Trigger set up!");

            m_tr.iDelay = 0;						// for LA2000P
            m_tr.iExtClk = 1;						// 1: Use Internal Clock
            m_tr.iFlag = LARunClass.TR_PRETRIG;
            m_tr.iFreq = (uint)(200E6);
            m_tr.iFreqHi = (int)((UInt64)200E6 >> 32);

            if(sequential == "1")
                m_tr.iPassCount = 1;					// 用來做reset count
            else
                m_tr.iPassCount = 0;

            m_tr.iTrPos = 50;						// Trigger signal located at point 50
            m_tr.iWidth = 0;                        // for LA2000P

            /* if (!this.ckTransMode.Checked)  //Standard conventional storage
                 m_giHwMode = LARunClass.LA_HW_MODE.HW_200M_9CH;
             else//Transitional storage 
                 m_giHwMode = LARunClass.LA_HW_MODE.HW_200M_32CH_TR;*/
            m_giHwMode = LARunClass.LA_HW_MODE.HW_200M_36CH;
            //gfTrMode = this.ckTransMode.Checked;
            gfTrMode = false;

            //Select HW mode
            if (!m_LARun.ulaSDKSetHwInfo((int)LARunClass.LA_HW_SETTING.SET_TL_MODE, (int)m_giHwMode))
            {
                ShowErrorCode();
                return;
            }

            //Select Channel mask
            /*byte[] iChannelMask = new byte[32];
			Array.Clear(iChannelMask, 0, 32);
			iChannelMask[0] = 0x08 | 0x10; //Mask channel 3, 4, 5, ignore all value change in these channels
			if (!m_LARun.ulaSDKSetChannelMask(iChannelMask, 32))
			{
				ShowErrorCode();
				return;
			}*/

            //Set H/W filter
            /*	int iFilterTime_ns = 20;	//20ns
                Int64 i64ChFilterOnOff = 0;
                i64ChFilterOnOff |= 0x01 << 0;	//Set CH0 Filter on
                i64ChFilterOnOff |= 0x01 << 5;	//Set CH5 Filter on
                if (!m_LARun.ulaSDKSetHwFilter(i64ChFilterOnOff, iFilterTime_ns))
                {
                    ShowErrorCode();
                    return;
                }*/

            if (!gfTrMode)  //memory setting not required in transitional storage mode
            {
                // Just to know the LA depth pre channel
                int iSamplesPerCh = m_LARun.ulaSDKGetMaxSamplesNum();
                Debug.WriteLine("sampelsPerCh: " + iSamplesPerCh);

                // I just need 2000 samples
                if (!m_LARun.ulaSDKSetSamplesNum(100000)) // 2000 // Set 2000 samples m_LARun.ulaSDKSetSamplesNum(2000)
                {
                    ShowErrorCode();
                    return;
                }
                // Get the buffer size(in bytes) for 2000 samples
                m_iCurSize = m_LARun.ulaSDKGetBufferSizeInBytes();
                Debug.WriteLine("Wave array size: " + m_iCurSize);
                m_lpiWave = new UInt32[m_iCurSize];
            }

            //Set Trigger position
            /*if (!gfTrMode)
                m_tr.iTrPos = 1000 / 2000;          // 1000 / 2000			// Trigger signal located at 50%, 2000samples -> 1000
            else
            {
                int iSamplesPerCh = m_LARun.ulaSDKGetMaxSamplesNum();
                m_tr.iTrPos = iSamplesPerCh / 2;
            }*/

            Console.WriteLine("Start Capture!");
            if (!m_LARun.ulaSDKCapture(ref m_tr))
            {
                ShowErrorCode();
                return;
            }

            /*MainTimerClock = new DispatcherTimer();
            //Creates a timerClock and enables it
            MainTimerClock.Interval = new TimeSpan(100);
            MainTimerClock.IsEnabled = true;
            MainTimerClock.Tick += new EventHandler(MainTimerClockProc);
            lbStatusDisplay.Text = "Capturing...";*/

            MainTimerClock = new System.Threading.Timer(new TimerCallback(MainTimerClockProc), null, 0, 100);
        }

        public void MainTimerClockProc(object obj)
        {
            //Console.WriteLine("Enter the timer Procedure!");
            //Check Trigger ready
            if (m_LARun.ulaSDKIsTriggerReady() != false)
                Console.WriteLine("Capturing...Triggered");
            else
                Console.WriteLine("Capturing...");
            // Wait Data ready
            if (m_LARun.ulaSDKIsCaptureReady() != false)
            {
                MainTimerClock.Dispose();
                Console.WriteLine("Capture finished!");

                // When data ready then read it.
                if (!gfTrMode)
                {
                    if (!m_LARun.ulaSDKGetBusData(31, 0, m_lpiWave, m_iCurSize, 0))
                    {
                        ShowErrorCode();
                        return;
                    }
                    getWaveData = true;
                    Debug.WriteLine(String.Join("\n", m_lpiWave));
                }
               /* else
                {//Collect data to a text file, no waveform drawing here
                    ReadTrWaveAndWriteFile();
                }
                Invalidate();*/
            }
            //getWaveData = true;
        }

        private void LAStop()
        {
            MainTimerClock.Dispose();
            Console.WriteLine("stop the LA!");
            if (!m_LARun.ulaSDKStopCapture())
            {
                ShowErrorCode();
                return;
            }
            if (!gfTrMode)
            {
                if (!m_LARun.ulaSDKGetBusData(31, 0, m_lpiWave, m_iCurSize, 0))
                {
                    ShowErrorCode();
                    return;
                }
            }
            /*else
            {//Collect data to a text file, no waveform drawing here
                ReadTrWaveAndWriteFile();
            }*/
            //if (!m_LARun.ulaSDKGetBusData(7, 0, m_lpiWave, m_iCurSize, 0)) // Stop capture       
            //{
            //    ShowErrorCode();
            //    return;
            //}
        }
        private void saveAsLaw()
        {
            Console.WriteLine("Save the law file!");
            if (!m_LARun.ulaSDKSaveAsLawFile(homeworkPathLaw + ".law"))
                ShowErrorCode();
        }

        private void SaveWithTemplateLaw()
        {
            if (!m_LARun.ulaSDKSaveAsLawFileWithTemplate("C:\\git-repos\\seniorproject\\test_code\\test.law", "SPI_Test.law"))
                ShowErrorCode();
        }

        private void ShowErrorCode()
        {
            int iErrorCode = m_LARun.ulaSDKGetLastError();
            csErrorString = "ErrorCode = " + ((LA_ErrorCode.ErrorCode)iErrorCode).ToString();
            Console.WriteLine(csErrorString);
        }

        /*private void testTimerProc(object obj)
        {
            Console.WriteLine("test timer");
        }*/

        private void writeWaveTxt()
        {
            Int64 x;
            try
            {
                //Open the File
                StreamWriter sw = new StreamWriter(homeworkPath, false, Encoding.UTF8);

                //Write wave data
                for (x = 0; x < m_iCurSize; x++)
                {
                    sw.WriteLine(m_lpiWave[x]);
                }

                //close the file
                sw.Close();
            }
            catch (Exception e)
            {
                Console.WriteLine("Error: " + e.Message);
            }
        }

        private void run_Main(string hwName,string pgvName,string sequen)
        {
            m_LARun = new LARunClass();
            m_giHwMode = LARunClass.LA_HW_MODE.HW_200M_36CH;
            gfTrMode = false;
            byte[] szBuf = System.Text.Encoding.ASCII.GetBytes("12345" + "\0");
            int iSize = szBuf.Count();
            int c = 0;
            //homeworkPath = "C:\\git-repos\\ours\\CloudLab\\server\\file\\" + className + "\\" + hwName;
            PGVName = pgvName;
            HWName = hwName;
            homeworkPath = hwName + "\\" + pgvName + ".txt";
            homeworkPathLaw = hwName + "\\" + pgvName;
            sequential = sequen;

            GetHW();
            Thread.Sleep(5000);
            LACapture();
            Thread.Sleep(15000);
            /*while (!getWaveData)
            {
                Console.WriteLine("Doesn't get the wave data yet!");
            }
            ;*/
            //if(getWaveData != true)  //如果波型太少，記憶體沒滿，就直接存下來。
            LAStop();
            saveAsLaw();
            writeWaveTxt();
           // MainTimerClock = new System.Threading.Timer(new TimerCallback(testTimerProc), null, 0, 1000);
            //Thread.Sleep(5000);
        }

        static void Main(string[] args)
        {
            Program run = new Program();

            run.run_Main(args[0],args[1],args[2]);
            Console.WriteLine("This is the Program END!!!");
            //Console.WriteLine(args[0]);
            //Console.ReadLine();
        }
    }
}
