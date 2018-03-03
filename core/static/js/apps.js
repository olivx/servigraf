$(function(){

    setInterval(function(){ 
        $('#alert-message').fadeTo(500, 0).slideUp(500, function(){
            $(this).remove()
        });
    }, 5000);


    $(".modal").modal({
		backdrop: 'static',
		keyboard: false,
		show: false
	})

    // ajustar
   $('.documento').each(function(){
        var documento = ''
        if ($(this).is('th')){
            documento = $(this).text();
        }

        if ($(this).is('input')){
            documento = $(this).val();
        }

        doc = documento.replace(/[\.\-\/ ]+/g, '')
        if (doc.length == 14 ){

             $('.documento').mask('00.000.000/0000-00', {reverse: true});
        }else{
            $('.documento').mask('000.000.000-00', {reverse: true});
        }
   });

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
                if(data.disable_all){
                    $('#cliente-modal input').attr('disabled','disabled');
                    $('#cliente-modal textarea').attr('disabled','disabled');
                    $('#cliente-modal select').attr('disabled','disabled');
                    $('#cliente-modal input[name=csrfmiddlewaretoken]').removeAttr('disabled');
                }
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
                        $('.message').html(data.message)
                        $('#cliente-modal').modal('hide');

                    }else{
                        $('#cliente-modal .modal-content').html(data.html_form);
                        tipo = $('select').val()
                        if(tipo  == 2){
                            $('.documento').mask('000.000.000-00', {reverse: true});
                        }else{
                            $('.documento').mask('00.000.000/000-00', {reverse: true});
                        }
                    }
                }
        });
    return false;
    };


    function deleteClientForm(){
        var form =  $(this);
            $.ajax({
                url:  form.attr('action'),
                type: form.attr('method'),
                data: form.serialize(),
                dataType: 'json',
                beforeSend:function(){

                    var x = confirm('Você realmente deseja desativar esse cliente ?')
                    if (x == false){
                        return false;
                    }

                },
                success: function(data){
                    if(data.is_form_valid){

                        $('#cliente-table tbody').html(data.html_table);
                        $('.message').html(data.message)
                        $('#cliente-modal').modal('hide');

                    }else{
                        $('#cliente-modal .modal-content').html(data.html_form);
                        tipo = $('select').val()
                        if(tipo  == 2){
                            $('.documento').mask('000.000.000-00', {reverse: true});
                        }else{
                            $('.documento').mask('00.000.000/000-00', {reverse: true});
                        }
                    }
                }
        });
    return false;
    };

     $('#cliente-modal').on('change', 'select', function(){
            var _select = $(this);
            if(_select.val() == 2){
                $('form').find('#div-razao-social label').text('Nome:');
                $('form').find('#div-nome-fantasia label').text('Sobre Nome:');
                $('form').find('#div-documento label').text('CPF:');
                $('.documento').val('')
                $('.documento').mask('000.000.000-00', {reverse: true});
            }else{
                $('form').find('#div-razao-social label').text('Razão Social:');
                $('form').find('#div-nome-fantasia label').text('Nome Fantasia:');
                $('form').find('#div-documento label').text('CNPJ:');
                $('.documento').val('')
                $('.documento').mask('00.000.000/0000-00', {reverse: true});
            }
        });

     $("#cliente-modal").on("shown.bs.modal", function (e) {
        $('.documento').mask('00.000.000/0000-00', {reverse: true});
        $('select').on('change', function(){
            var _select = $(this);
            if(_select.val() == 2){
                $('.documento').val('')
                $('.documento').mask('000.000.000-00', {reverse: true});
            }else{
                $('.documento').val('')
                $('.documento').mask('00.000.000/0000-00', {reverse: true});
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
    $('#cliente-modal').on('submit', '.js-delete-client-form', deleteClientForm);


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
                if(data.disable_all){

                    $('input').attr('disabled', 'disabled')
                    $('textarea').attr('disabled', 'disabled')
                    $('select').attr('disabled', 'disabled')
                    $('#modal .btn-primary').attr('disabled', 'disabled')
                    $('input[name=csrfmiddlewaretoken]').removeAttr('disabled')


                }
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
                    $('.messages').html(data.message);
                    $('#modal').modal('hide');


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

            beforeSend: function(){
                var x = confirm('Voce realmente deseja Desativar esse cliente ?')
                if(x == false){
                    return false;
                }
            },
            success: function(data){

                $('#contact-table tbody').html(data.html_table);
                $('.pagination').html(data.html_pagination)
                $('#modal').modal('hide');
                $('.messages').html(data.message);

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

                    $('.messages').html(data.message)
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

                $('.messages').html(data.message)
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

                if(data.disable_all){

                   $("#modal-product input").attr('disabled','disabled');
                   $("#modal-product select").attr('disabled','disabled');
                   $("#modal-product textarea").attr('disabled','disabled');
                   $("#modal-product input[name=csrfmiddlewaretoken]").removeAttr('disabled');


                }
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
                   $('.money').mask("#.##0,00", {reverse: true});

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
    $('#modal-product').on('submit' , '.js-form-product-delete', function(){

        var x = confirm('Tem certeza que deseja deletar esse produto ?')
        if(x == false){
            return false;
        }

    });

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

                $('#modal-group .modal-content').html(data.html_form);
                $('#modal-group .modal-content tbody').html(data.html_table);

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
                    $('#modal-group .modal-content').html(data.html_form);
                    $('#modal-group .modal-content tbody').html(data.html_table);

                }else{
                    $('#modal-group .modal-content').html(data.html_form);
                    $('#modal-group .modal-content tbody').html(data.html_table);


                }

                $('.modal .modal-body').css('overflow-y','auto');
                $('.modal .modal-body').css('height' , $(window).height() * 0.7 );

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

        $.ajax({
            url: 'api/product/group/list/',
            dataType: 'json',

            success: function(data){

                 var json_obj = $.parseJSON(data.groups);
                 if(json_obj ){
                    $('select[name=group] option').remove();
                   // <option value="" selected="selected">---------</option>
                    $('select[name=group]').append($('<option>').text('---------').
                    attr('selected','selected').attr('value',''));
                 }
                 $.each(json_obj, function(key, obj){
                      $('select[name=group]').append($('<option>').text(obj.fields.group).attr('value', obj.pk));

                 });

            }

        });
    });

    // open from product form
    $('#modal-product').on('click', '.js-open-modal-group', loadGroupProductForm);

    // open from grou form link or clean form from button limpar
    $('#modal-group').on('click', '.js-open-modal-group', loadGroupProductForm);

    // save update and delete from group from
    $('#modal-group').on('click', '.js-save-modal-group', saveGroupProductForm);
    $('#modal-group').on('click', '.js-update-modal-group', saveGroupProductForm);

    // delete group
    $('#modal-group').on('click', '.js-delete-modal-group', function(){

        var btn = $(this);
        var form = $('form');
        $.ajax({
            url: btn.attr('data-url'),
            type: 'post',
            data: form.serialize(),
            dataType: 'json',
            beforeSend: function(){
                var _confirm = confirm('Você realmente deseja deletar esse Grupo');
                if(_confirm == false){
                    return false;
                }
            },
            success: function(data){

                if(data.is_form_valid){
                    $('#modal-group .modal-content').html(data.html_form);
                    $('#modal-group .modal-content tbody').html(data.html_table);
                }else{
                        $('#modal-group .modal-content').html(data.html_form);
                        $('#modal-group .modal-content tbody').html(data.html_table);
                    }

                $('.modal .modal-body').css('overflow-y','auto');
                $('.modal .modal-body').css('height' , $(window).height() * 0.7 );
            }
        });
    return false;
    });

    function filter(element, selector) {
        var value = $(element).val().toUpperCase();
        $(selector +" li").each(function () {
            if ($(this).text().toUpperCase().indexOf(value)> -1) {
                $(this).show();
            } else {
                $(this).hide();
            }
        });
     }

   $('.search_client_list').keyup(function(){
        filter(this, '#list-client');
    })
   $('.search_services_list').keyup(function(){
        filter(this, '#list-services');
    })

   $('.modal').on('hidden.bs.modal', function(e){
        $('input').val('')
   }) ;




    function ProjectClientLoad(){

        btn =  $('.js-project-create-client')

        $.ajax({

            url: btn.attr('data-url'),
            dataType: 'json',

            beforeSend: function(){
                $('#modal-projeto-cliente').modal('show')
            },
            success: function(data){
                $('#modal-projeto-cliente .modal-dialog').html(data.html_form)
                $('.autocomplete').autocomplete({
                    // appendTo: '',
                    minLength: 3,
                    source: $('#autocomplete-cliente-project-url').attr('data-url'),
                    select: function(event, ui) {
                        $('#modal-projeto-cliente #id_client').val(ui.item.id)
                    }
                });
            }
        });
    return false;
    }

    function ProjectClientCreate(){
        var form =  $(this)
        $.ajax({

            dataType: 'json',
            data: form.serialize(),
            url: form.attr('action'),
            type: form.attr('method'),

            error: function (xhr, ajaxOptions, thrownError) {
                console.log(xhr.status)
                console.log(thrownError)
                console.log(xhr.responseText)
            },
            success: function(data){

                if(data.is_form_valid ==  true ){

                    $('.message').html(data.message)
                    $('#modal-projeto-cliente').modal('hide')
                    $('.js-list-client-project').html(data.list_client)

                }else{

                    $('.message_modal').html(data.message)
                    $('#modal-projeto-cliente .modal-dialog').html(data.html_form)
                    $('.autocomplete').autocomplete({
                        appendTo: 'autocomplete_projeto_cliente',
                        minLength: 3,
                        source: $('#autocomplete-url').attr('data-url')
                    });

                }
            }

        });
     return false;
    }


   $('.js-project-create-client').on('click' , ProjectClientLoad);
   $('#modal-projeto-cliente').on('submit', '.js-form-create-project-client', ProjectClientCreate);


    function ProjectServiceLoad(){
        var btn = $(this)

        $.ajax({
            url: btn.data('url'),
            dataType: 'json',

            beforeSend: function(){
                $('#modal-add-service-to-project').modal('show')
                
            },
            success: function(data){
                
                $('#modal-add-service-to-project .modal-dialog').html(data.html_form)
                $('.autocomplete').autocomplete({
                    // appendTo: '', 
                    minLength: 3,
                    source: $('#autocomplete-service-project-url').data('url'),
                    select: function(event, ui){
                        $('.js-porject-service-price').val(ui.item.price)
                        $('.js-porject-service-id').val(ui.item.id)
                    }
                })

            }

        })

    }

    function ProjectServiceCreate(e){
        var form = $(this)

        $.ajax({
            url: form.attr('action'),
            type: form.attr('method'),
            data: form.serialize(),
            dataType: 'json', 

            success: function(data){
                if (data.is_form_valid == true){
                    $('.message').html(data.message)
                    $('.js-list-service-project').html(data.service_list)
                    $('#modal-add-service-to-project').modal('hide')
                
                }else{
                    $('#modal-add-service-to-project .modal-dialog').html(data.html_form)
                    $('#modal-add-service-to-project .modal-dialog .form-html').addClass('has-error')
                    $('.message_modal').html(data.message)

                    $('.autocomplete').autocomplete({
                        minLength: 3,
                        source: $('#autocomplete-service-project-url').data('url'),
                        select: function(event, ui){
                            $('.js-porject-service-price').val(ui.item.price)
                            $('.js-porject-service-id').val(ui.item.id)
                        }
                    })

                }
            }
        });
        return false
    }
    $('#add-service-to-project').on('click', ProjectServiceLoad)  
    $('#modal-add-service-to-project').on('submit', '.js-form-create-prject-service', ProjectServiceCreate)   
       

    $('.js-project-create-client').click(function(){
        $('#modal-projeto').modal('show')
    });


    $('.js-deactive-client-project').click(function(){
        $('#modal-deactivate-project').modal('show');
        var client_id  =  $(this).attr('id')
        $('#modal-deactivate-project input[type=hidden]').val(client_id)

    });

    $('.js-deactive-service-project').click(function(){
        $('#modal-service-deactivate-project').modal('show');
        var service_id  =  $(this).attr('id')
        data_url = $(this).data('url')
        text = $(this).data('text')
        $('#modal-service-deactivate-project .js-project-service-to-delete p').text(text)
        $('#modal-service-deactivate-project .js-project-delete-service').attr('action', data_url)
        $('#modal-service-deactivate-project input[name=service]').val(service_id)

    });


    $('.btn-project-deactive').click(function(event) {
        /* Act on the event */
        $('#deactive-project').modal('show')
        $('#deactive-project input[name=deactive-input-project]').val($(this).data('id'))

        $('#deactive-project #div-deactivate').html($(this).data('name'))
        $('#deactive-project .js-project-deactive-form').attr('action', $(this).data('url'))


    });

    $('.btn-project-update').click(function(event) {
        /* Act on the event */
        $('#update-project').modal('show')
        $('#update-project input[name=deactive-input-project]').val($(this).data('id'))

        $('#update-project #id_title_update').val($(this).data('name'))
        $('#update-project #id_desc_update').val($(this).data('desc'))
        $('#update-project #id_project').val($(this).data('id'))
        $('#update-project .js-project-update-form').attr('action', $(this).data('url'))


    });



});
