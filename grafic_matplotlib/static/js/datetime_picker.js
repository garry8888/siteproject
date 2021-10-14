<script type="text/javascript">
    $(function () {
        // инициализация datetimepicker7 и datetimepicker8
        $("#datetimepicker7").datetimepicker();
        $("#datetimepicker8").datetimepicker({
            useCurrent: true
        });
        $("#datetimepicker7").on("dp.change", function (e) {
            $('#datetimepicker8').data("DateTimePicker").minDate(e.date);
        });
        $("#datetimepicker8").on("dp.change", function (e) {
            $('#datetimepicker7').data("DateTimePicker").maxDate(e.date);
        });
    });
</script>