module trafficLight(clk,reset,LightA,LightB);

input clk,reset;
output [2:0] LightA,LightB;

reg [3:0] next_count, current_count;
reg [2:0] LightA,LightB;
reg [1:0] cs, ns;

always @(*) begin
    case (cs)
    2'b00:
    begin
        next_count = (current_count < 4'd8) ? current_count + 4'd1 :4'd1;
        ns = (current_count < 4'd8) ? 2'b00 : 2'b01;
    end
    2'b01:
    begin
        next_count = (current_count <4'd3) ? current_count + 4'd1 : 4'd1;
        ns = (current_count < 4'd3) ? 2'b01 :2'b10;
    end
    2'b10:
    begin
        next_count = (current_count <4'd10) ? current_count + 4'd1 : 4'd1;
        ns = (current_count < 4'd10) ? 2'b10 :2'b11;
    end
    2'b11:
    begin
        next_count = (current_count <4'd3) ? current_count + 4'd1 : 4'd1;
        ns = (current_count < 4'd3) ? 2'b11 :2'b00;
    end 
    endcase
    
end

always @(posedge clk or negedge reset) begin
    if(!reset)
    begin
        current_count <= 4'd1;
        cs <= 2'b00;
    end
    else
    begin
        current_count <= next_count;
        cs <= ns;
    end
end

always @(*) begin
begin
    case (cs)
    2'b00:
    begin
        LightA = 3'b001;
        LightB = 3'b100;
    end
    2'b01:
    begin
        LightA = 3'b010;
        LightB = 3'b100;
    end
    2'b10:
    begin
        LightA = 3'b100;
        LightB = 3'b001;
    end
    2'b11:
    begin
        LightA = 3'b100;
        LightB = 3'b010;
    end  
    
    endcase
end

end

endmodule
