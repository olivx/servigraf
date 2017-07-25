$(function(){

    function loadClientForm(){
         var btn = $(this);
        $.ajax({
            url: btn.attr('data-url'),
            type: 'GET',
            dataType: 'json',
            beforeSend: function(){
                $('#cliente-modal').modal('show');
            },
            success: function(data){
                $('#cliente-modal .modal-content').html(data.html_form);
            }
        });
    };

    function saveClientForm(){  
        var form =  $(this);
            $.ajax({
                url:  form.attr('action'),
                type: form.attr('method'),
                data: form.serialize(),
                dataType: 'json',

                success: function(data){
                    if(data.is_form_valid){

                        $('#cliente-table tbody').html(data.html_table);
                        $('#cliente-modal').modal('hide');
                        alert(data.message)

                    }else{
                        alert(data.message)
                        $('#cliente-modal .modal-content').html(data.html_form);
                    }
                }
        });
    return false;
    };

    $("#cliente-modal").on("shown.bs.modal", function (e) {

        $('select').on('change', function(){
            var _select = $(this);
            if(_select.val() == 2){
                $('[href="#section-contact"]').closest('li').hide();
                $('form').find('#div-razao-social label').text('Nome:');
                $('form').find('#div-nome-fantasia label').text('Sobre Nome:');
                $('form').find('#div-documento label').text('CPF:');


            }else{
                $('[href="#section-contact"]').closest('li').show();
                $('form').find('#div-razao-social label').text('Razão Social:');
                $('form').find('#div-nome-fantasia label').text('Nome Fantasia:');
                $('form').find('#div-documento label').text('CNPJ:');
            }
        });
    });


    // save cliente form
    $('.js-open-form-cliente').click(loadClientForm);
    $('#cliente-modal').on('submit', '.js-save-client-form', saveClientForm);

    // update cliente form
    $('#cliente-table').on('click' , '.js-update-modal-cliente', loadClientForm);
    $('#cliente-modal').on('submit', '.js-update-client-form', saveClientForm);

    // delete client
    $('#cliente-table').on('click', '.js-delete-modal-cliente', loadClientForm);
    $('#cliente-modal').on('submit', '.js-delete-client-form', saveClientForm);


    // contact methods

    function loadContactForm(){
        var btn =  $(this);
        $.ajax({
            url:        btn.attr('data-url'),
            type:       'GET',
            dataType:   'json',

            beforeSend: function(){
                $('#modal').modal('show');
            },
            success: function(data){
                $('#modal .modal-content').html(data.html_form);
            }
        });
    };

    function saveContactForm(){
        var form = $(this);
        $.ajax({
            dataType: 'json',
            url:  form.attr('action'),
            type: form.attr('method'),
            data: form.serialize(),

            success: function(data){
                if(data.is_form_valid){
                    $('#contact-table tbody').html(data.html_table);
                    $('#client-form').html(data.html_form);
                    $('#modal').modal('hide');

                    alert(data.message);

                }else{

                    $('#modal .modal-content').html(data.html_form);
                }
            }
        });
    return false;
    };

    // contact save
    $('.js-open-contact-form',).click(loadContactForm);
    $('#contact-table').on('click', '.js-open-contact-form', loadContactForm);
    $('#modal').on('submit', '.js-client-contact-form', saveContactForm);

    // update


    // email formset

    //remove item email formset
    $('#modal').on('click' , '#remove-email', function(){
        count =  $('#email-formset').children().length;
        if (count > 1){
            $('#email-formset div').last().remove();

            // update valid total forms
            $('#id_email-TOTAL_FORMS').attr('value' , count);
        }else{

            alert('Opa! 1 é minimo de email field para o formulario.')
        }
    });

    // add item email formset
    $('#modal').on('click' , '#add-email', function(){

        var count = $('#email-formset').children().length;
        var tmp = $("#contact-email").html();
        var new_email_form = tmp.replace(/__prefix__/g, count);
        $("div#email-formset").append(new_email_form);

         // update form email valid total forms
         $('#id_email-TOTAL_FORMS').attr('value', count + 1);

         // animate to scroll
        $('#modal, .modal-body').animate({
            scrollTop: $("#add-email").position().top-200
          }, 1500);

    });

    // add item telefone formset
    $('#modal').on('click', '#add-telefone', function(){

        var count =  $('#telefone-formset').children().length;
        var tmp = $('#contact-telefone').html();
        var new_telefone_form =  tmp.replace(/__prefix__/g, count);
        $('div#telefone-formset').append(new_telefone_form);

        // upate validate formset
        $('#id_telefone-TOTAL_FORMS').attr('value', count + 1)

        // animate to scroll
        $('#modal, .modal-body').animate({
            scrollTop: $('#add-telefone').position().top-200
        }, 1500);

    });

    // remove formset element
    $('#modal').on('click', '#remove-telefone', function(){

        count =  $('#telefone-formset').children().length;
        if( count > 1){

            $('#telefone-formset .form-group').last().remove();
            $('#id_telefone-TOTAL_FORMS').attr('value', count);

        }else{

            alert('Opa! 1 é minimo de telefone field para o formulario.')
        }
    });


});