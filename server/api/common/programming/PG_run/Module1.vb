Imports System.Threading

Module Module1
    Dim glDevice As Long = -1
    Dim m_pgsi As New PGSDK_Class.PGSI
    Dim DeviceText As String
    Dim FileText As String

    Private Sub BnGetHW_Click()
        Dim i, ID As Long
        Dim szModel As String
        If PGSDK_Class.upgInitEx(0, 0) Then
            i = PGSDK_Class.upgGetStatus()  '得到一個32位元的值
            ID = i And 255          ' 與 11111111 做 and 得到機器型號
            glDevice = i >> 16      '?? 向右移動16位元
            If ID <= 0 Then
                If glDevice <> -1 Then
                    PGSDK_Class.upgShutdown()
                    glDevice = -1
                End If
            End If
            If (glDevice = -1) Then
                Console.WriteLine("Error:No Hardware!")

                Return
            End If
            If (ID = &H10) Then
                szModel = "PKPG2116+ (512K)"
            ElseIf (ID = &H6) Then
                szModel = "PG2050 (512K)"
            Else
                szModel = "Other Models"
            End If
            DeviceText = szModel
        End If
    End Sub

    Private Sub BnStart_Click()
        Dim lResult As Long
        Dim lRet As Long
        Dim lFileType As Long
        Dim Str, Str1, Str2 As String

        Str = FileText
        Str1 = Str.Substring(Str.Length() - 4)
        Str2 = Str1.ToUpper()
        If (StrComp(Str2, ".PGW") = 0) Then
            lFileType = 0
        ElseIf (StrComp(Str2, ".PGV") = 0) Then
            lFileType = 1
        Else
            Console.WriteLine("Error:Unknown file type!")
            Return
        End If
        PGSDK_Class.upgAdjVolt(0, 5000)
        PGSDK_Class.upgAdjVolt(1, 5000)
        m_pgsi.iPodVolt(0) = 5000
        m_pgsi.iPodVolt(1) = 5000

        lResult = PGSDK_Class.upgStart(Str, lFileType, m_pgsi)
        lRet = (lResult And &HFFFF)

        If (lRet = 0) Then

        ElseIf (lRet = 1) Then
            Console.WriteLine("Error:File Not Found.")
        ElseIf (lRet = 2) Then
            Console.WriteLine("Error:File Reading Error.")
        ElseIf (lRet = 3) Then
            Console.WriteLine("Error:File Type Error or Not Support.")
        ElseIf (lRet = 4) Then
            Console.WriteLine("Error:File Format Error.")
        ElseIf (lRet = 5) Then
            Console.WriteLine("Error:File Version is too old.")
        ElseIf (lRet = 6) Then
            Console.WriteLine("Error:Memory Not Enough.")
        ElseIf (lRet = 7) Then
            Console.WriteLine("Error:Singal Name confuse in PGV file.")
        ElseIf (lRet = 8) Then
            Console.WriteLine("Error:Too many channel to be defined.")
        ElseIf (lRet = 9) Then
            Console.WriteLine("Error:PGV Time Stamp Error.", "Error")
        ElseIf (lRet = 10) Then
            Console.WriteLine("Error:Can't use Time Stamp and INTERVAL or FREQUENCY at same time.")
        ElseIf (lRet = 11) Then
            Console.WriteLine("Error:No Signal Name in PGV File.")
        ElseIf (lRet = 12) Then
            Console.WriteLine("Error:Over PG hardware memory depth.")
        ElseIf (lRet = 13) Then
            Console.WriteLine("Error:No Time Stamp in Time Stamp mode.")
        ElseIf (lRet = 14) Then
            Console.WriteLine("Error:No channel assigned for some signal.")
        ElseIf (lRet = 99) Then
            Console.WriteLine("Error:No Hardware.")
        ElseIf (lRet = &H8001) Then
            Console.WriteLine("Error: Use close frequency for system clock.")

        Else
            MsgBox("Error:Critical Error.")
        End If
        'PGSDK_Class.upgStop()
        'PGSDK_Class.upgStart("oringinaltest2.pgv", lFileType, m_pgsi)
        'PGSDK_Class.upgStart("oringinaltest3.pgv", lFileType, m_pgsi)
    End Sub

    Private Sub BnStop_Click()
        PGSDK_Class.upgStop()

    End Sub

    Private Sub BnShutdown_Click()
        PGSDK_Class.upgStop()
        PGSDK_Class.upgShutdown()
        Console.WriteLine("This is the end!")

        DeviceText = ""
        glDevice = -1
    End Sub

    Private Sub BnBrowse_Click(ByVal File As String)
        '   Dim fd As OpenFileDialog = New OpenFileDialog()
        '  fd.Title = "Open PG file..."
        ' fd.InitialDirectory = "C:\"
        'fd.Filter = "PG Waveform Files(*.pgw;*.pgv)|*.pgw;*.pgv|All Files(*.*)|*.*||"
        'fd.FilterIndex = 1
        'fd.RestoreDirectory = True

        ' If fd.ShowDialog() = DialogResult.OK Then
        FileText = File
        'End If

    End Sub
    Public Sub Main(ByVal cmdArgs() As String)
        'Console.WriteLine(cmdArgs(0))
        'Console.WriteLine(cmdArgs(1))
        Dim timePass As Double

        timePass = cmdArgs(1) + 3000

        FileText = cmdArgs(0)
        m_pgsi.Initialize()
        BnGetHW_Click()
        'BnBrowse_Click(cmdArgs(0))
        BnStart_Click()
        Thread.Sleep(timePass)
        BnShutdown_Click()
    End Sub

End Module
