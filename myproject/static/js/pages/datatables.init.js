$(document).ready(function(){$("#datatable").DataTable({
        "paging":   false,
        "ordering": false,
        "info":     false
    });var a=$("#datatable-buttons").DataTable({lengthChange:!1,buttons:["copy","excel","pdf"]});$("#key-datatable").DataTable({keys:!0}),$("#selection-datatable").DataTable({select:{style:"multi"}}),a.buttons().container().appendTo("#datatable-buttons_wrapper .col-md-6:eq(0)")});
