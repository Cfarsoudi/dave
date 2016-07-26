package dave;
import java.util.*;
import java.text.*;

public class DiscoveryOneTest{
    public static SimpleDateFormat 	format = new SimpleDateFormat("dd-M-yyyy hh:mm:ss");

	public static Date startDateTime = format.parse("08-17-2012 13:13:13");
	public static Date endDateTime  = format.parse("08-18-2012 15:26:59");

	private dave.DiscoveryOne discoveryOne;
	/*@BeforeClass
	public static void SetUp(){
		startDateTime = format.parser("08-17-2012 13:13:13");
		endDateTime = format.parser("08-18-2012 15:26:59");
	}*/

	@Test 
	public void TestCalcElapsedDays(){
		assertEquals(1, discoveryOne.CalcElapsedDays(startDateTime, endDateTime));
	    System.out.println("@Test: OneCalcElapsedDays");

	}
}