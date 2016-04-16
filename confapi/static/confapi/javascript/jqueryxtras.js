var temp = [];
var map = new Object();

function myFunction(endpoint) {
//alert( "Handler for .change() called." );

    var z_https = 1;
    if ($('#https').is(":checked"))
    {
        z_https = 0;
    };
    //alert( protocol);
    //var endpoint = $( ".selectEndPoint" ).val();
    var i = 0;
    var apiFunctions;
    //alert( '/api_functions?endpoint=' + endpoint + '&z_https=' + z_https );
    $.getJSON('/api_functions?endpoint=' + endpoint + '&z_https=' + z_https, function(data){
        //$.getJSON('/confapi/api_functions', function(data){
        //$.getJSON('http://192.168.56.12/zabbix/api_functions.json', function(data){
        var functionsNames = '';
        var i;
        for (i=0; i<Object.keys(data).length; i++) {
            functionsNames += '<option>' +  Object.keys(data)[i] + '</option>';
        }
        functionsNames += "<option>" +  'Editar...' + "</option>";
        $(".selectFunction").empty().append($(functionsNames)).hide().fadeIn(700);



        $(document).on('change', ".selectFunction", function() {
            $(".txt").removeClass('animated bounceInRight');
            var selectedFunction = $(this).val()[0];
            var boxes = "<div class='txt'><h3 class='text-center header_help'>3. Informe os Parâmetros</h3><br><div class='container text_boxes'>";


            if (selectedFunction == 'Editar...'){
                $('#selector-input-function').removeClass('animated swing');
                boxes += "<div class='col-md-8'><textarea class='form-control' rows=12' required placeholder='Informe o hash de parâmetros aqui!'></textarea></div><br><br><br><br><br><br><br><br><br><br><br><br><br><br>";
                $('#selector-input-function').fadeOut("400", function(){
                    var textbox = $("<div class='textFunction'><input type='text' class='form-control' id='function' name='function' value='host.get' required placeholder='method' onClick='this.select();'></div>");
                    $(this).html(textbox).hide().fadeIn(400).addClass('animated swing');
                });
            }
            else {
                var endString1;
                var endString2;
                var options;
                var i=0;
                //for (var i=0; i<Object.keys(data[selectedFunction]).length; i++) {
                for (var key in data[selectedFunction]) {
                    if(i%2) {
                        boxes += "<div class='col-md-4'>";
                        endString2 = "</div></div><br>";
                    }
                    else {
                        boxes += "<div class= 'row'><div class='col-md-4'>";
                        endString2 = "</div>";
                    }

                    if (data[selectedFunction][key]['type'] == 0) {
                        boxes += "<input type='text' class='form-control'";
                        endString1 = ">";
                    }
                    //JSON
                    else if (data[selectedFunction][key]['type'] == 1) {
                        boxes += "<textarea class='form-control'";
                    }
                    //select
                    else if (data[selectedFunction][key]['type'] == 2) {
                        boxes += "<div id='red-tooltip'>"
                        boxes += "<select class='form-control sel' data-toogle='tooltip' title='Escolha um valor para este campo!' id='"+Object.keys(data[selectedFunction])[i]+"'";
                        options = "<option selected='true' disabled style='display:none;'>"+ key +"</option>";
                        if (data[selectedFunction][key]['default']){
                            options += '<option>' + data[selectedFunction][key]['default'] + '</option>';
                        }
                        for (var j=0; j<data[selectedFunction][key]['values'].length; j++) {
                            if (data[selectedFunction][key]['values'][j] != data[selectedFunction][key]['default']){
                                options += '<option>' + data[selectedFunction][key]['values'][j]  + '</option>';
                            }
                        }
                        //Populate form fields
                        //temp[i] = ""+Object.keys(data[selectedFunction])[i];
                        //$("#alarm").val("no");

                        endString1 = ">" + options + "</select>" + "</div>";
                    }


                    if (!(data[selectedFunction][key]['optional'])) {
                        boxes += " required ";
                    }

                    if (data[selectedFunction][key]['default']) {
                        boxes += " id=\""+Object.keys(data[selectedFunction])[i]+"\" name=\""+Object.keys(data[selectedFunction])[i]+"\"placeholder=\""+Object.keys(data[selectedFunction])[i]+" (default: " + data[selectedFunction][key]['default'] + ") "+"\" ";

                        //Populate form fields
                        temp[i] = ""+Object.keys(data[selectedFunction])[i];
                        if(sessionStorage.getItem(temp[i]) != null && sessionStorage.getItem(temp[i]) != "undefined"){
                            $("#alarm").val("no");
                            boxes += "value=\""+sessionStorage.getItem(temp[i])+"\"";
                        }
                    }
                    //JSON
                    else {
                        if (data[selectedFunction][key]['type'] == 1) {
                            boxes += " id=\""+Object.keys(data[selectedFunction])[i]+"\" name=\""+Object.keys(data[selectedFunction])[i]+"\"placeholder=\""+Object.keys(data[selectedFunction])[i]+" (json)\" ";
                            
                            //Populate form fields
                            temp[i] = ""+Object.keys(data[selectedFunction])[i];
                            if(sessionStorage.getItem(temp[i]) != null && sessionStorage.getItem(temp[i]) != "undefined"){
                                endString1 = ">"+sessionStorage.getItem(temp[i])+"</textarea>";
                            }
                            else{
                                endString1 = "></textarea>";   
                            }
                        }
                        else {
                            boxes += " id=\""+Object.keys(data[selectedFunction])[i]+"\" name=\""+Object.keys(data[selectedFunction])[i]+"\"placeholder=\""+Object.keys(data[selectedFunction])[i]+"\" ";
                            
                            //Populate form fields
                            temp[i] = ""+Object.keys(data[selectedFunction])[i];
                            if(sessionStorage.getItem(temp[i]) != null && sessionStorage.getItem(temp[i]) != "undefined"){
                                boxes += "value=\""+sessionStorage.getItem(temp[i])+"\"";
                            }
                        }
                    }
                    boxes += endString1 + endString2;
                    i++;
                }

                //Bug com o novo método
                // if (Object.keys(data[selectedFunction]).length%2) {
                //     boxes += "<br><br>";
                // }
            }
        boxes += "<br><br><div class= 'row'><div class='col-md-4 col-md-offset-2'><button type='submit' class='btn-lg btn-block btn-primary'>3. Envie os Parâmetros!</button></div></div></div></div>";

        $(".txt").fadeOut(400, function(){ $(this).html(boxes).hide().fadeIn(400).addClass('animated bounceInRight');});
        });

    });
}

function getSelectEndpoint(){
    var endpoint = $( ".selectEndPoint" ).val();
    myFunction(endpoint);
}

function getEditarEndpoint(){
    //alert($('#endpointBox').val());
    var endpoint = $('#endpointBox').val();
    myFunction(endpoint);
}

$(document).ready(function(){


    $(document).on('click', '.comingSoon', function(){
        event.preventDefault();
        $(this).tooltip("show");
    });

    getSelectEndpoint();

    $( "#useForm" ).submit(function(event) {

        //Hashing values -- Populate form fields
        for (i = 0; i < temp.length; i++) {
            var text = $("#"+temp[i]+"").val();
            sessionStorage.setItem(temp[i], text);
        }

        $('.sel').each(function(){
            if (!($(this).val())) {
                $(this).tooltip("show");
                $(this).change(function() { $(this).tooltip('destroy'); });

                event.preventDefault();
            }
        });

    });

    var selector = $(".selectEndPoint");
    $(document).on('dblclick', ".textEndPoint", function() {
        $('#selector-inputbox').fadeOut("400", function(){

            $(this).html(selector.val($('#endpointBox').val())).hide().fadeIn(400);
            getSelectEndpoint();
        });
    });

    var textbox_value = $(".selectEndPoint").val();
    $(document).on('change', ".selectEndPoint", function() {
        $(this).each(function(){
            if ($(this).val() == 'Editar...') {
                $('#selector-inputbox').removeClass('animated swing');
                $('#selector-inputbox').fadeOut("400", function(){
                    var inputbox = $("<div class='textEndPoint'><input type='text' class='form-control' id='endpointBox' name='z_endpoint' value='" + textbox_value + "' placeholder='endpoint' onClick='this.select();'></div>");
                    $(this).html(inputbox).hide().fadeIn(400).addClass('animated swing');
                    $('#endpointBox').on('blur', function() {
                        getEditarEndpoint();
                    });
                });
            }else{
                getSelectEndpoint();
                textbox_value = $(".selectEndPoint").val();
            }
        });
    });

    var functions = $(".selectFunction");
    $(document).on('dblclick', ".textFunction", function() {
        $('#selector-input-function').fadeOut("400", function(){
            $(this).html(functions.val($('#function').val())).hide().fadeIn(400);
        });
    });

});


