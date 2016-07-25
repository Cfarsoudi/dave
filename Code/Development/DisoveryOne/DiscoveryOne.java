import org.jsoup.Jsoup;
import org.jsoup.helper.Validate;
import org.jsoup.nodes.Document;
import org.jsoup.nodes.Element;
import org.jsoup.select.Elements;

import java.util.Date;
import java.io.BufferedWriter;
import java.io.BufferedReader;
import java.io.File;
import java.io.FileWriter;
import java.io.FileReader;
import java.io.IOException;
import java.io.FileNotFoundException;
import java.text.SimpleDateFormat;

public class DiscoveryOne{
	public static final long SECONDSINMILLI =     1000;
	public static final long MINUTESINMILLI =    60000;
	public static final long HOURSINMILLI   =  3600000;
	public static final long DAYSINMILLI    = 86400000;

	public static void main(String[] args) throws Exception  {
		//Check to see if the user specified an input file and a output file
		if(args.length != 2){
			System.out.println("Error: Wrong amount arguments : "+args.length);
			System.exit(0);
		}
		
		//Grabbing Parameters
		String input  = args[0]; 
    	String output = args[1];

    	//Date for timestamping
       	Date date = new Date();

       	//Timing Vars
       	Date startTime;
       	Date endTime;
       	//Initializng the input and output files
    	BufferedReader reader = new BufferedReader(new FileReader(input));
    	BufferedWriter writer = new BufferedWriter(new FileWriter(output));

    	//start reading the inputfile
    	String url = reader.readLine();
    	//Get Start time
    	startTime = new Date();
    	//Output to log
    	System.out.println(String.format("%s : Started Fetching Links From == %s",
    									 startTime, input));
    	try {
    		while (url != null) {
    			//check if the url is not a link ot a pdf
    			if(!url.contains(".pdf")){
    				//Out to log
    				date = new Date();
	    			System.out.println(String.format("%s : Started Fetching ===== %s ",
	    							   date.toString(), url));
	    			//grab the html for url
	    			Document doc = Jsoup.connect(url).get();
	    			//grab only the pre tags in doc
					Elements scriptLines = doc.select("pre");

					//Print to output file
					for (Element line : scriptLines) {
						writer.write(line.text());
						writer.newLine();						
					}
				}
				// read next line in file
				url = reader.readLine();
    		}
    		//Out to log
    		date = new Date();
    		System.out.println(String.format("%s : Done Fetching ===== %s", 
    			  							 date.toString(), url));
    	}catch(IOException ex){    
    		date = new Date();		
            System.out.println(ex);
            System.out.println(String.format("Error === %s : %s ",url,date.toString()));

		}finally{
			//close files
			writer.close();
			reader.close();

			endTime = new Date();
			// Calculate time elapse
			long elapsedDays    = CalcElapsedDays(startTime , endTime);
			long elapsedHours   = CalcElapsedHours(startTime , endTime);
			long elapsedMinutes = CalcElapsedMinutes(startTime , endTime);
			long elapsedSeconds = CalcElapsedSeconds	(startTime , endTime);
			//report
			System.out.println(String.format("Start Time : %s", startTime.toString()));
			System.out.println(String.format("End Time   : %s", endTime.toString()));
			System.out.println(String.format("Time Elapsed : %d days , %d hours, %d minutes, %d seconds", 
								elapsedDays,elapsedHours,elapsedMinutes,elapsedSeconds));
		}
	}

	public static long CalcElapsedDays(Date startDate, Date endDate){
	
		//milliseconds
		long different = endDate.getTime() - startDate.getTime();
		long elapsedDays = different / DAYSINMILLI;
		return elapsedDays;
	}

	public static long CalcElapsedHours(Date startDate, Date endDate){
	
		//milliseconds
		long different = (endDate.getTime() - startDate.getTime());
		different = different - CalcElapsedDays(startDate, endDate)*DAYSINMILLI;
		
		long elapsedHours = different / HOURSINMILLI;
		
		return 	elapsedHours;
	}

	public static long CalcElapsedMinutes(Date startDate, Date endDate){
	
		//milliseconds
		long different = (endDate.getTime() - startDate.getTime());
		different = different - CalcElapsedDays(startDate, endDate)*DAYSINMILLI;
		different = different - CalcElapsedHours(startDate, endDate)*HOURSINMILLI;
		
		long elapsedMinutes = different / MINUTESINMILLI;
		
		return 	elapsedMinutes;
	}

	public static long CalcElapsedSeconds(Date startDate, Date endDate){
	
		//milliseconds
		long different = (endDate.getTime() - startDate.getTime());
		different = different - CalcElapsedDays(startDate, endDate)*DAYSINMILLI;
		different = different - CalcElapsedHours(startDate, endDate)*HOURSINMILLI;
		different = different - CalcElapsedMinutes(startDate, endDate)*MINUTESINMILLI;
		
		long elapsedSeconds = different / SECONDSINMILLI;
		
		return 	elapsedSeconds;
	}
}