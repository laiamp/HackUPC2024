$(document).ready(function() {
    $('#searchEvents').click(function() {
        var ciutat = $('#cityInput').val();
        var categoria = $('#categoryInput').val();
        var data = $('#dataInput').val();
        
        $.ajax({
            type: "GET",
            url: "https://app.ticketmaster.com/discovery/v2/events.json",
            data: {
                city: ciutat,
                classificationName: categoria,
                startDateTime: data + "T00:00:00Z",
                endDateTime: data + "T23:59:59Z",
                apikey: "YfAAYQzOHJMlfY1v9swWxAksA7dSk3YG"
            },
            async: true,
            dataType: "json",
            success: function(json) {
                $('#listaEventos').empty(); 
                
                if (json._embedded && json._embedded.events && json._embedded.events.length > 0) {
                    json._embedded.events.forEach(function(evento) {
                        $('#listaEventos').append('<li>' + evento.name + '</li>');
                    });
                } else {
                    $('#listaEventos').append('<li>No se encontraron eventos.</li>');
                }
            },
            error: function(xhr, status, err) {
                console.error("Error al obtener eventos:", err);
            }
        });
    });
});
