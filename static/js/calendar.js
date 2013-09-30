$(document).ready(function() {
    $( "#datepicker" ).datepicker({
        onSelect: function(dateText, inst) {
                    var date1 = $.datepicker.parseDate($.datepicker._defaults.dateFormat, $("#input1").val());
                    var date2 = $.datepicker.parseDate($.datepicker._defaults.dateFormat, $("#input2").val());
                    if (!date1 || date2) {
                        $("#input1").val(dateText);
                        $("#input2").val("");
                        $(this).datepicker("option", "minDate", dateText);
                    } else {
                        $("#input2").val(dateText);
                        $(this).datepicker("option", "minDate", null);
                    }
                }
    });
  });