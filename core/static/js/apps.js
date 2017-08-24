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
                    $('.pagination_contact').html(data.html_pagination)
                    $('#modal').modal('hide');

                    alert(data.message);

                }else{

                    $('#modal .modal-content').html(data.html_form);
                }
            }
        });
    return false;
    };

    function deleteContactForm(){
        var form = $(this);
        $.ajax({

            dataType:'json',
            data: form.serialize(),
            url: form.attr('action'),
            type: 'post',

            success: function(data){

                $('#contact-table tbody').html(data.html_table);
                $('.pagination').html(data.html_pagination)
                $('#modal').modal('hide');
                alert(data.message);

            }

        });
     return false;
    };

    $('.js-open-contact-form',).click(loadContactForm);

    $('#modal').on('submit', '.js-open-contact-form', saveContactForm);

    // contact update
    $('#contact-table').on('click', '.js-open-contact-form-update', loadContactForm);
    $('#modal').on('submit', '.js-client-contact-form-update', saveContactForm);

    // deactivation contact
    $('#contact-table').on('click' , '.js-open-contact-form-delete', loadContactForm);
    $('#modal').on('submit', '.js-contact-form-delete', deleteContactForm);


    // email formset
    // add item email formset
    $('#modal').on('click' , '#add-email', function(){

        var count = $('#email-formset').children().length;
        var tmp = $("#contact-email").html();
        var new_email_form = tmp.replace(/__prefix__/g, count);
        $("div#email-formset").append(new_email_form);

         // update form email valid total forms
         $('#id_email-TOTAL_FORMS').attr('value', parseInt(count) );

         // animate to scroll
        $('#modal, .modal-body').animate({
            scrollTop: $("#add-email").position().top-200
          }, 1500);

    });

     //remove item email formset
    $('#modal').on('click' , '#remove-email', function(){
        count =  $('#email-formset').children().length;
        if (count > 1){
            $('#email-formset div').last().remove();
            $('#id_email-TOTAL_FORMS').attr('value' , parseInt(count -1 ));
        }else{

            alert('Opa! 1 é minimo de email field para o formulario.')
        }
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
            $('#id_telefone-TOTAL_FORMS').attr('value', count - 1);

        }else{

            alert('Opa! 1 é minimo de telefone field para o formulario.')
        }
    });


    // method end
    function loadEnderecoForm(){
        btn = $(this);

        $.ajax({

            url: btn.attr('data-url'),
            type: 'get',
            dataType: 'json',

            beforeSend: function(){
                $('#modal').modal('show');
            },
            success: function(data){
                $('#modal .modal-content').html(data.html_form);

                if(data.disable_all){

                    $.each($('#modal input') , function(){
                        $("#modal input").attr('disabled','disabled');
                        $("#modal textarea").attr('disabled','disabled');
                        $("#modal select").attr('disabled','disabled');
                         $('input[name=csrfmiddlewaretoken]').removeAttr('disabled');
                    });

                }else{
                    $.each($('#modal input') , function(){
                        $("#modal input").removeAttr('disabled');
                    });


                }

            }

        });

    };

    function saveEndForm(){

        // liberar para que o cliente seja enviado no form.
        $("#id_cliente").removeAttr('disabled');

        var form = $(this);
        $.ajax({

            dataType: 'json',
            url: form.attr('action'),
            data: form.serialize(),
            type: form.attr('method'),

            success: function(data){

                if(data.is_form_valid){

                    alert('Endereço salvo com sucesso!')

                    $('#address-table tbody').html(data.html_table);
                    $('.pagination_end').html(data.html_pagination);
                    $('#modal').modal('hide');

                }else{

                    $('#modal .modal-content').html(data.html_form);

                }

            }

        });
    return false;
    };

    //  abre o formulario de cadastro do endereço de cliente
    $('.js-open-end-form').click(loadEnderecoForm );
    $('#modal').on('submit', '.js-save-end-form', saveEndForm);

    $('#address-table').on('click', '.js-open-end-form-update' , loadEnderecoForm );
    $('#modal').on('submit' , '.js-update-end-form', saveEndForm)

    $('#address-table').on('click', '.js-open-end-form-delete' , loadEnderecoForm );
    $('#modal').on('submit' , '.js-delete-end-form', function(){

        var form  = $(this);
        $.ajax({

            dataType: 'json',
            data: form.serialize(),
            url: form.attr('action'),
            type: form.attr('method'),

            beforeSend: function(){
                var ask =  confirm('Deseja realmente desativar esse formulario ?')
                if(ask  == false){
                    return false;
                }

            },
            success: function(data){

                alert('Endereço foi desativado, mas ainda pode ser visto na area administrativa do sistema.');

                $('#address-table tbody').html(data.html_table);
                $('.pagination_end').html(data.html_pagination);

                $('#modal').modal('hide');
            }

        });
      return false;
      });



    //  busca o cep pelo viaCep
    $('#modal').on('click', '.search_cep' , function(){

        var cep =  $('.input_cep').val();
        cep  = cep.replace('-', '')
        var validacep = /^[0-9]{8}$/;


       // para ceps validos
        if(validacep.test(cep)){

            $.getJSON("http://viacep.com.br/ws/"+ cep +"/json/?callback=?", function(dados) {
                if (!("erro" in dados)) {

                    $('#id_cep').mask('00000-000');

                    // update endereco
                    $('#id_endereco').val(dados.logradouro);
                    $('#id_bairro').val(dados.bairro);
                    $('#id_cidade').val(dados.localidade);
                    $('#id_uf').val(dados.uf);
                }
                else {
                    //CEP pesquisado não foi encontrado.
                    alert("CEP não encontrado.");
                }
            }); // get json

        }// valida cep
        else{

            alert('CEP invalido. \nverifique o campo CEP.')
        }

    });

    // limpa o modal de endereço
    $('#modal').on('click', '.form_cleaned' , function(){
             $.each($('#modal input'),function(){
                $(this).val('');
            });

            $('textarea').val('');

    });


    function loadProductForm(){

       var btn = $(this);

       $.ajax({

            type:'get',
            dataType:'json',
            url: btn.attr('data-url'),

            beforeSend: function(){

                $('#modal-product').modal('show');

            },
            success: function(data){

                $('#modal-product .modal-content').html(data.html_form)
                $('.money').mask("#.##0,00", {reverse: true});
            }


       });

    };

    function saveProductForm(){
        var form = $(this);

        var valor = $('.money').val();
        $('.money').val(valor.replace('.','').replace(',', '.'))



        $.ajax({
            dataType: 'json',
            url: form.attr('action'),
            type: form.attr('method'),
            data: form.serialize(),

            success: function(data){

                if(data.is_form_valid){

                    $('#messages').html(data.message)
                    $('#table-product tbody').html(data.html_table);
                    $('#modal-product').modal('hide');

                }else{

                   $('#modal-product .modal-content').html(data.html_form);

                }
            }

        });
    return false;
    };

    // product
    $('#product-create').click(loadProductForm);
    $('#modal-product').on('submit' , '.js-form-product-save' , saveProductForm);

    $('#table-product').on('click' , '.js-open-form-update', loadProductForm);
    $('#modal-product').on('submit', '.js-form-product-update', saveProductForm);

    $('#table-product').on('click' , '.js-open-form-delete', loadProductForm);

    //group

    function loadGroupProductForm (){

        var btn = $(this);
        $.ajax({
            url: btn.attr('data-url'),
            type: 'get',
            dataType: 'json',

           beforeSend: function(){

                $('#modal-product').modal('hide');
                $('#modal-group').modal('show');

           },
            success: function(data){
                $('#form-group').html(data.html_form);
                $('#table-group tbody').html(data.html_table);
            }

        });

    };

    function saveGroupProductForm(){

        var form = $('form');
        var btn = $(this);
        $.ajax({
            url: btn.attr('data-url'),
            type: 'post',
            data: form.serialize(),
            dataType: 'json',

            success: function(data){
                if(data.is_form_valid){
                    $('#form-group').html(data.html_form);
                    $('#modal-group  tbody').html(data.html_table);

                }else{
                    $('#form-group').html(data.html_form);

                }
            }
        });
       return false;
    };

    $('#modal-group').on('shown.bs.modal', function(){
        $('.modal .modal-body').css('overflow-y','auto');
        $('.modal .modal-body').css('height' , $(window).height() * 0.7 );
    });

    $('#modal-group').on('hidden.bs.modal', function () {
        $('#modal-product').modal('show');
    });

    $('#modal-product').on('click', '.js-open-modal-group', loadGroupProductForm);
    $('#modal-group').on('click', '.js-save-modal-group', saveGroupProductForm);
    $('#table-group').on('click', '.js-open-modal-group', loadGroupProductForm);




});