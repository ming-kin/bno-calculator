$(document).ready(function() {
  // Initialize datepicker
  $(".datepicker").datepicker({
    dateFormat: 'yy-mm-dd',
    changeMonth: true,
    changeYear: true
  });

  // Function to add a new absence period
  $("#add").click(function() {
    $("#absences").append('<div class="absence"><input type="text" name="absence_from[]" class="datepicker"><input type="text" name="absence_to[]" class="datepicker"><button type="button" class="remove">Remove</button></div>');
    $(".datepicker").datepicker({
      dateFormat: 'yy-mm-dd',
      changeMonth: true,
      changeYear: true
    });
  });

  // Function to remove an absence period
  $("#absences").on('click', '.remove', function() {
    $(this).parent().remove();
  });

  // Validate form before submission
  $("form").submit(function(event) {
    var isValid = true;
    $(".datepicker").each(function() {
      if (!$(this).val()) {
        isValid = false;
      }
    });
    if (!isValid) {
      event.preventDefault();
      alert("Please fill in all date fields before submitting.");
    }
  });
});