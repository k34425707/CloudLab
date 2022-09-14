Imports System
Imports System.Runtime.InteropServices

Public Class PGSDK_Class
    <StructLayoutAttribute(LayoutKind.Sequential)> _
    Public Structure PGSI
        Public iFreq As Integer
        Public iFreqMode As Integer
        Public iPGVRecord As Integer
        <MarshalAs(UnmanagedType.ByValArray, SizeConst:=6)> Public iPodVolt As Integer()
        <MarshalAs(UnmanagedType.ByValArray, SizeConst:=119)> Public iRes As Integer()
        Public Sub Initialize() 'Must Call this function before use
            ReDim iPodVolt(6 - 1)
            ReDim iRes(119 - 1)
        End Sub
    End Structure


    <DllImport("PgRun.dll", EntryPoint:="upgInitEx")> _
    Public Shared Function upgInitEx(ByVal lModel As Long, ByVal lSlot As Long) As Boolean
    End Function

    <DllImport("PgRun.dll", EntryPoint:="upgGetStatus")> _
    Public Shared Function upgGetStatus() As Long
    End Function

    <DllImport("PgRun.dll", EntryPoint:="pgInterfaceName")> _
    Public Shared Function pgInterfaceName(ByVal lDevice As Long, ByVal pbNull As Byte, ByVal lItem As Long, ByRef pszBuf As Long, ByVal lSize As Long) As Boolean
    End Function

    <DllImport("PgRun.dll", EntryPoint:="upgAdjVolt")> _
    Public Shared Function upgAdjVolt(ByVal lGroup As Long, ByVal lMilliVolt As Long) As Long
    End Function

    <DllImport("PgRun.dll", EntryPoint:="upgStart")> _
    Public Shared Function upgStart(ByVal szFileName As String, ByVal lFileType As Long, ByRef pPgsi As PGSI) As Long
    End Function
    <DllImport("PgRun.dll", EntryPoint:="upgStop")> _
    Public Shared Function upgStop() As Boolean
    End Function
    <DllImport("PgRun.dll", EntryPoint:="upgShutdown")> _
    Public Shared Function upgShutdown() As Boolean
    End Function
    <DllImport("PgRun.dll", EntryPoint:="upgKeyEvent")> _
    Public Shared Function upgKeyEvent() As Boolean
    End Function

End Class


