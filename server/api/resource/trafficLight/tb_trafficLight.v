module tb_trafficLight();
//inputs
reg clk,reset;
//outputs
wire [2:0] LightA,LightB;

//用來寫檔案的變數
integer err,fp;
reg [320:0] str1;
//

trafficLight TL0(clk,reset,LightA,LightB);


//設定clk頻率
always #5 clk = ~clk;

initial
begin
    //
    clk = 0;
    reset = 1;
    //以上可以自己做inputs數值初始化

    //for Debug
	$monitor($time, " LightA Sig = %b LightB Sig = %b", LightA, LightB);

    //以下是固定寫法，有些可以自己更改
    //開啟文件
    fp = $fopen("traffic.pgv");    //()裡面的檔名可以自己更改
    err = $ferror(fp, str1);
    //確認文件可開啟
    if(!fp)
    begin
        $display("Couldn't open the file! \r");
        $display("File2 descriptor is: %h.", fp ); //0
        $display("Error2 number is: %h.", err );   //非零值
        $display("Error2 info is: %s.", str1 );     //非零值
        $stop;
    end
    //設定pgv檔
    //write pgv file initial settings
    $fdisplay(fp, "INPUTS PG_Function DATA;");
    $fdisplay(fp, "ASSIGN DATA 2..1;");      //這個的"1..0"可根據input大小改變，例:如果input有5條，可以改成ASSIGN DATA 4..0;
    $fdisplay(fp, "RADIX AUTO;");
    $fdisplay(fp, "UNIT Us;");               //LA的單位時間大小，通常設US會比較好觀察
    $fdisplay(fp, "PATTERN");
    $fdisplay(fp, "0.0> 8FFh 0h");
    $fdisplay(fp, "1.0> 2FFh 0h");
    $fdisplay(fp, "2.0> 900h 0h");          //以上三行是在初始化LA，照抄即可不必更改

    //以上是固定寫法，有些可以自己更改


    // 以下可以開始寫testbench的向量了

    //fmonitor代表 如果寫在裡面的變數一有變化，那就會跟著寫入檔案中
    #5 $fmonitor(fp,"%0d.0> 000h %b%bb",$time,clk,reset);
    //set clock
    #20 reset = 0;
    #30 reset = 1; 
    #430 $fdisplay(fp, ";"); 
    $fclose(fp);
    $stop;
    //
end

endmodule

