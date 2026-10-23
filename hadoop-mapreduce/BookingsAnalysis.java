import java.io.IOException;
import java.util.Locale;
import java.util.ArrayList;
import java.util.List;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.FileSystem;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.NullWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;

public class BookingsAnalysis {

    private static final String HEADER =
            "Date,Time,Booking_ID,Booking_Status";

    public enum DatasetCounters {
        DATA_ROWS
    }

    public static class CountMapper
            extends Mapper<LongWritable, Text, NullWritable, NullWritable> {

        public void map(LongWritable key, Text value, Context context)
                throws IOException, InterruptedException {

            String line = value.toString();

            if (!line.trim().isEmpty() && !line.startsWith(HEADER)) {
                context.getCounter(DatasetCounters.DATA_ROWS).increment(1);
            }
        }
    }

    public static class BookingMapper
            extends Mapper<LongWritable, Text, Text, Text> {

        private static final String[] COLUMNS = {
            "Date", "Time", "Booking_ID", "Booking_Status",
            "Customer_ID", "Vehicle_Type", "Pickup_Location",
            "Drop_Location", "V_TAT", "C_TAT",
            "Canceled_Rides_by_Customer", "Canceled_Rides_by_Driver",
            "Incomplete_Rides", "Incomplete_Rides_Reason",
            "Booking_Value", "Payment_Method", "Ride_Distance",
            "Driver_Ratings", "Customer_Rating"
        };

        private String field(String[] row, int index) {
            return index < row.length ? row[index].trim() : "";
        }

        private double number(String value) {
            try {
                if (value.isEmpty()) return Double.NaN;
                double n = Double.parseDouble(value);
                return Double.isFinite(n) ? n : Double.NaN;
            } catch (NumberFormatException e) {
                return Double.NaN;
            }
        }

        private String[] parseCSV(String line) {
            List<String> fields = new ArrayList<>();
            StringBuilder current = new StringBuilder();
            boolean quoted = false;

            for (int i = 0; i < line.length(); i++) {
                char ch = line.charAt(i);

                if (ch == '"') {
                    if (quoted && i + 1 < line.length()
                            && line.charAt(i + 1) == '"') {
                        current.append('"');
                        i++;
                    } else {
                        quoted = !quoted;
                    }
                } else if (ch == ',' && !quoted) {
                    fields.add(current.toString());
                    current.setLength(0);
                } else {
                    current.append(ch);
                }
            }

            fields.add(current.toString());
            return fields.toArray(new String[0]);
        }

        private void emit(Context context, String key, double count,
                double success, double valueSum, double valueCount,
                double distanceSum, double distanceCount,
                double driverSum, double driverCount,
                double customerSum, double customerCount,
                double maximumDistance)
                throws IOException, InterruptedException {

            String metrics = count + "\t" + success + "\t" + valueSum
                    + "\t" + valueCount + "\t" + distanceSum
                    + "\t" + distanceCount + "\t" + driverSum
                    + "\t" + driverCount + "\t" + customerSum
                    + "\t" + customerCount + "\t" + maximumDistance;

            context.write(new Text(key), new Text(metrics));
        }

        private void count(Context context, String key)
                throws IOException, InterruptedException {
            emit(context, key, 1, 0, 0, 0, 0, 0,
                    0, 0, 0, 0, 0);
        }

        public void map(LongWritable key, Text value, Context context)
                throws IOException, InterruptedException {

            String line = value.toString();

            if (line.trim().isEmpty() || line.startsWith(HEADER)) {
                return;
            }

            String[] r = parseCSV(line);

            if (r.length < 19) {
                context.getCounter("DATA_QUALITY",
                        "INVALID_COLUMN_COUNT").increment(1);
            }

            String date = field(r, 0);
            String time = field(r, 1);
            String status = field(r, 3);
            String vehicle = field(r, 5);
            String customerCancel = field(r, 10);
            String driverCancel = field(r, 11);
            String incomplete = field(r, 12);
            String incompleteReason = field(r, 13);
            String valueText = field(r, 14);
            String payment = field(r, 15);
            String distanceText = field(r, 16);
            String driverRatingText = field(r, 17);
            String customerRatingText = field(r, 18);

            double bookingValue = number(valueText);
            double distance = number(distanceText);
            double driverRating = number(driverRatingText);
            double customerRating = number(customerRatingText);

            boolean success = status.equalsIgnoreCase("Success");

            double validValue = Double.isNaN(bookingValue) ? 0 : bookingValue;
            double valueN = Double.isNaN(bookingValue) ? 0 : 1;
            double validDistance = Double.isNaN(distance) ? 0 : distance;
            double distanceN = Double.isNaN(distance) ? 0 : 1;
            double validDriver = Double.isNaN(driverRating) ? 0 : driverRating;
            double driverN = Double.isNaN(driverRating) ? 0 : 1;
            double validCustomer = Double.isNaN(customerRating) ? 0 : customerRating;
            double customerN = Double.isNaN(customerRating) ? 0 : 1;

            // 1. Booking status counts and percentages.
            if (!status.isEmpty()) {
                count(context, "01_STATUS|" + status);
            }

            // 2. Vehicle-wise booking and success statistics.
            if (!vehicle.isEmpty()) {
                emit(context, "02_VEHICLE|" + vehicle,
                        1, success ? 1 : 0, validValue, valueN,
                        validDistance, distanceN, validDriver, driverN,
                        validCustomer, customerN, validDistance);
            }

            // 3. Revenue and payment summaries.
            if (!payment.isEmpty()) {
                emit(context, "03_PAYMENT|" + payment,
                        1, success ? 1 : 0, validValue, valueN,
                        0, 0, 0, 0, 0, 0, 0);
            }

            if (!Double.isNaN(bookingValue) && !status.isEmpty()) {
                emit(context, "03_VALUE_BY_STATUS|" + status,
                        1, success ? 1 : 0, bookingValue, 1,
                        0, 0, 0, 0, 0, 0, 0);
            }

            // 4. Customer and driver cancellation analysis.
            if (status.toLowerCase(Locale.ROOT).contains("cancel")
                    || status.equalsIgnoreCase("Driver Not Found")) {
                count(context, "04_CANCELLATION|" + status);
            }

            if (!customerCancel.isEmpty()
                    && !customerCancel.equalsIgnoreCase("No")) {
                count(context, "04_CUSTOMER_CANCEL|" + customerCancel);
            }

            if (!driverCancel.isEmpty()
                    && !driverCancel.equalsIgnoreCase("No")) {
                count(context, "04_DRIVER_CANCEL|" + driverCancel);
            }

            // 5. Ratings and incomplete rides.
            if (!Double.isNaN(driverRating) && !vehicle.isEmpty()) {
                emit(context, "05_DRIVER_RATING|" + vehicle,
                        1, 0, 0, 0, 0, 0, driverRating, 1,
                        0, 0, 0);
            }

            if (!Double.isNaN(customerRating) && !vehicle.isEmpty()) {
                emit(context, "05_CUSTOMER_RATING|" + vehicle,
                        1, 0, 0, 0, 0, 0, 0, 0,
                        customerRating, 1, 0);
            }

            if (incomplete.equalsIgnoreCase("Yes")
                    || status.toLowerCase(Locale.ROOT).contains("incomplete")) {
                count(context, "05_INCOMPLETE_RIDE");
                count(context, "05_INCOMPLETE_REASON|"
                        + (incompleteReason.isEmpty()
                        ? "(missing reason)" : incompleteReason));
            }

            // 6. Date, time, month and distance analysis.
            if (!date.isEmpty()) {
                count(context, "06_DATE|" + date);

                if (date.length() >= 7) {
                    count(context, "06_MONTH|" + date.substring(0, 7));
                }
            }

            if (time.length() >= 2) {
                try {
                    int hour = Integer.parseInt(time.substring(0, 2));

                    if (hour >= 0 && hour <= 23) {
                        count(context, "06_HOUR|"
                                + time.substring(0, 2) + ":00");
                    } else {
                        count(context, "06_INVALID|Time");
                    }
                } catch (NumberFormatException e) {
                    count(context, "06_INVALID|Time");
                }
            }

            if (!Double.isNaN(distance) && !vehicle.isEmpty()) {
                emit(context, "06_DISTANCE|" + vehicle,
                        1, 0, 0, 0, distance, 1,
                        0, 0, 0, 0, distance);
            }

            // 7. Missing-value and invalid-value analysis.
            for (int i = 0; i < COLUMNS.length; i++) {
                if (field(r, i).isEmpty()) {
                    count(context, "07_MISSING|" + COLUMNS[i]);
                }
            }

            if (!Double.isNaN(bookingValue) && bookingValue < 0) {
                count(context, "07_INVALID|Negative_Booking_Value");
            }

            if (!Double.isNaN(distance) && distance < 0) {
                count(context, "07_INVALID|Negative_Ride_Distance");
            }

            if (!Double.isNaN(driverRating)
                    && (driverRating < 0 || driverRating > 5)) {
                count(context, "07_INVALID|Driver_Rating");
            }

            if (!Double.isNaN(customerRating)
                    && (customerRating < 0 || customerRating > 5)) {
                count(context, "07_INVALID|Customer_Rating");
            }
        }
    }

    public static class BookingReducer
            extends Reducer<Text, Text, Text, Text> {

        private long totalRows;

        protected void setup(Context context) {
            totalRows = context.getConfiguration()
                    .getLong("bookings.total.rows", 0);
        }

        private String fmt(double value) {
            if (Math.abs(value - Math.rint(value)) < 0.000001) {
                return Long.toString((long) Math.rint(value));
            }
            return String.format(Locale.ROOT, "%.2f", value);
        }

        private String average(double sum, double count) {
            return count == 0 ? "N/A" : fmt(sum / count);
        }

        public void reduce(Text key, Iterable<Text> values, Context context)
                throws IOException, InterruptedException {

            String k = key.toString();
            double[] s = new double[11];

            for (Text value : values) {
                String[] parts = value.toString().split("\t", -1);

                for (int i = 0; i < Math.min(parts.length, s.length); i++) {
                    try {
                        double n = Double.parseDouble(parts[i]);

                        if (i == 10) {
                            s[i] = Math.max(s[i], n);
                        } else {
                            s[i] += n;
                        }
                    } catch (NumberFormatException ignored) {
                    }
                }
            }

            String result;

            if (k.startsWith("01_STATUS|")) {
                double percentage = totalRows == 0
                        ? 0 : s[0] * 100.0 / totalRows;

                result = "count=" + fmt(s[0])
                        + ", percentage=" + fmt(percentage) + "%";

            } else if (k.startsWith("02_VEHICLE|")) {
                double successRate = s[0] == 0
                        ? 0 : s[1] * 100.0 / s[0];

                result = "bookings=" + fmt(s[0])
                        + ", successes=" + fmt(s[1])
                        + ", success_rate=" + fmt(successRate) + "%"
                        + ", booking_value_sum=" + fmt(s[2])
                        + ", average_booking_value=" + average(s[2], s[3])
                        + ", average_distance=" + average(s[4], s[5])
                        + ", average_driver_rating=" + average(s[6], s[7])
                        + ", average_customer_rating=" + average(s[8], s[9]);

            } else if (k.startsWith("03_PAYMENT|")) {
                result = "bookings=" + fmt(s[0])
                        + ", successful_bookings=" + fmt(s[1])
                        + ", booking_value_sum=" + fmt(s[2])
                        + ", average_booking_value=" + average(s[2], s[3]);

            } else if (k.startsWith("03_VALUE_BY_STATUS|")) {
                result = "records_with_value=" + fmt(s[3])
                        + ", total_value=" + fmt(s[2])
                        + ", average_value=" + average(s[2], s[3]);

            } else if (k.startsWith("05_DRIVER_RATING|")) {
                result = "rated_records=" + fmt(s[7])
                        + ", average_driver_rating=" + average(s[6], s[7]);

            } else if (k.startsWith("05_CUSTOMER_RATING|")) {
                result = "rated_records=" + fmt(s[9])
                        + ", average_customer_rating=" + average(s[8], s[9]);

            } else if (k.startsWith("06_DISTANCE|")) {
                result = "records_with_distance=" + fmt(s[5])
                        + ", average_distance=" + average(s[4], s[5])
                        + ", maximum_distance=" + fmt(s[10]);

            } else {
                result = "count=" + fmt(s[0]);
            }

            context.write(key, new Text(result));
        }
    }

    public static void main(String[] args) throws Exception {

        if (args.length != 2) {
            System.err.println(
                    "Usage: BookingsAnalysis <input-path> <output-path>");
            System.exit(2);
        }

        Configuration conf = new Configuration();
        Path input = new Path(args[0]);
        Path output = new Path(args[1]);
        FileSystem fs = input.getFileSystem(conf);

        // Job 1: Count data rows, excluding the header.
        Job countJob = Job.getInstance(conf, "Bookings Row Count");
        countJob.setJarByClass(BookingsAnalysis.class);
        countJob.setMapperClass(CountMapper.class);
        countJob.setNumReduceTasks(0);
        countJob.setOutputKeyClass(NullWritable.class);
        countJob.setOutputValueClass(NullWritable.class);

        FileInputFormat.addInputPath(countJob, input);

        Path tempOutput = new Path(output.toString() + "_rowcount_tmp");

        if (fs.exists(tempOutput)) {
            fs.delete(tempOutput, true);
        }

        FileOutputFormat.setOutputPath(countJob, tempOutput);

        if (!countJob.waitForCompletion(true)) {
            System.err.println("Row count job failed.");
            System.exit(1);
        }

        long totalRows = countJob.getCounters()
                .findCounter(DatasetCounters.DATA_ROWS).getValue();

        fs.delete(tempOutput, true);

        // Job 2: Run the seven requested analysis categories.
        Configuration analysisConf = new Configuration();
        analysisConf.setLong("bookings.total.rows", totalRows);

        Job job = Job.getInstance(
                analysisConf, "Bookings Analysis");

        job.setJarByClass(BookingsAnalysis.class);
        job.setMapperClass(BookingMapper.class);
        job.setReducerClass(BookingReducer.class);

        job.setMapOutputKeyClass(Text.class);
        job.setMapOutputValueClass(Text.class);
        job.setOutputKeyClass(Text.class);
        job.setOutputValueClass(Text.class);

        FileInputFormat.addInputPath(job, input);

        if (fs.exists(output)) {
            System.err.println("Output path already exists: " + output);
            System.err.println("Remove it or choose another output path.");
            System.exit(2);
        }

        FileOutputFormat.setOutputPath(job, output);

        System.exit(job.waitForCompletion(true) ? 0 : 1);
    }
}