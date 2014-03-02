//package com.jjr.btcar;
//
//import org.apache.commons.lang.StringUtils;
//
//import java.io.BufferedReader;
//import java.io.IOException;
//import java.io.InputStreamReader;
//import java.util.List;
//import java.util.Map;
//
//public class App {
//
//    private static final String DEVICE = "/dev/tty.OBDLinkMX-STN-SPP";
//    private static final int BAUD = 115200;
//
//    public static void main( String[] args ) {
//
//        try {
//
//            Controller controller = new Controller();
//            controller.connect(DEVICE, BAUD);
//
//            if(!controller.verifyConnection()) {
//                controller.disconnect();
//                throw new RuntimeException("Couldn't verify connection to car. Aborting.");
//            }
//
//            controller.newSession();
//
//            do {
//
//                readLine("Baseline - Press ENTER when ready.");
//                controller.startRecording();
//
//                readLine("Press ENTER when you're about to make a change. Press ENTER again after.");
//                controller.markBefore();
//
//                readLine("Press ENTER after change.");
//                controller.stopRecording();
//
//                if(!readLine("Keep that run? [y]").contains("n")) {
//                    controller.saveRun();
//                }
//
//            } while(readLine("Again? [n]").contains("y"));
//
//            controller.disconnect();
//
//
//            Analyzer analyzer = new Analyzer();
//            Analyzer.Analysis analysis = analyzer.beforeAfter(controller.getSessionData());
//
//            analysis.getResults();
//            Map<String, Integer> map = analysis.getCardinalityMap();
//            for(String k : map.keySet()) {
//                List<Integer> cardinality = analysis.getCardinalityByRun(k);
//                System.out.println(k + " - " +
//                        StringUtils.join(cardinality, ", ")
//                        + " = " + map.get(k)
//                );
//            }
//
//        } catch (Exception e) {
//            throw new RuntimeException(e);
//        }
//
//    }
//
//    private static String readLine(String message) throws IOException {
//        System.out.print(message);
//        System.out.print(" ");
//        BufferedReader reader = new BufferedReader (new InputStreamReader(System. in));
//        return reader.readLine();
//    }
//
//}
//
