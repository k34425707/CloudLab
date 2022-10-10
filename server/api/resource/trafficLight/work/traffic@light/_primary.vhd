library verilog;
use verilog.vl_types.all;
entity trafficLight is
    port(
        clk             : in     vl_logic;
        reset           : in     vl_logic;
        LightA          : out    vl_logic_vector(2 downto 0);
        LightB          : out    vl_logic_vector(2 downto 0)
    );
end trafficLight;
