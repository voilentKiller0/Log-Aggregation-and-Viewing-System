

document.addEventListener('DOMContentLoaded', function() {
    // Get the input element
    var startdateTimeInput = document.getElementById('startdatetime');
    var enddateTimeInput = document.getElementById('enddatetime');

    // Set the current date and time as the default value
    var now = new Date();
    var year = now.getFullYear();
    var month = (now.getMonth() + 1).toString().padStart(2, '0'); // Months are zero-based
    var day = now.getDate().toString().padStart(2, '0');
    var hours = now.getHours().toString().padStart(2, '0');
    var minutes = now.getMinutes().toString().padStart(2, '0');
    var defaultDateTime = `${year}-${month}-${day}T${hours}:${minutes}`;
    
    startdateTimeInput.value = defaultDateTime;
    enddateTimeInput.value = defaultDateTime;

});

<script>
    $(document).ready(function () {
       $('.selectpicker').selectpicker();
    });
 </script>
 
