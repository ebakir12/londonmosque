odoo.define('event_registration_custom.event_registration', function (require) {

var ajax = require('web.ajax');
var core = require('web.core');
var Widget = require('web.Widget');
var publicWidget = require('web.public.widget');

var _t = core._t;

    $(document).on('click','button.btn-form',function(ev){
        ev.preventDefault();
        ev.stopImmediatePropagation();
        var valid = true;
        var form = ev.target.closest('form');
        var emails = [];
        var repeated_emails = [];
        var inputs_emails = $(form).find('input[type=email]');
        var selected_options = $(form).find('option:selected');
        $(form).find('.invalid-answer').addClass('o_hidden');
        $(form).find('.invalid-input').remove();
        var answer_ids = [];
        var answer_elem = {};
        var empty = $(form).find('input[required]').filter(function() {
            return this.value == '';
        });
        if (empty.length) {
            valid = false;
            $(empty[0]).focus()
            for(var m = 0; m < empty.length ; m++){
                $(empty[m]).after('<span style="color:red;" class="invalid-input">This field is required.</span>');
            }
        }

        for(var i = 0 ; i < inputs_emails.length ; i ++){
            var inpt = inputs_emails[i];
            var val = inpt.value;
            var re = /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
            if(val){
                if( !re.test(val) ){
                    valid = false;
                    $(inpt).after('<span style="color:red;" class="invalid-input">Invalid email.</span>');
                }
            }
            if(emails.includes(val)){
                repeated_emails.push(val);
            }else{
                emails.push(val);
            }
        }
        for(var j = 0 ; j < selected_options.length ; j ++){
            var option = selected_options[j];
            var val = parseInt(option.value);
            answer_ids.push(val);
            if(answer_elem[val]){
                answer_elem[val].push(option);
            }else{
                answer_elem[val] = [option];
            }

        }
	
	if(repeated_emails.length){
	    if(repeated_emails[0].value.length == 0){
		 repeated_emails = [];
		}
	}

        if(repeated_emails.length){
            valid = false;
            var repeated_str = repeated_emails.join(' - ');
            alert('You are already using the email ' + repeated_str + ' for this event registration .. Maximum 1 registration per person is allowed.');
        }else{
            var form_action = form['action'];
            var event_str = form_action.split('/')[4];
            var url = '/event/' + event_str + '/check_attendees_data';
            if(valid){
                ajax.jsonRpc(url, 'call', {'emails':emails,'answers':answer_ids}).then(function(res) {
                    if(res){
                        var repeated_emails = res['emails'];
                        var invalid_answers = res['answers'];
                        if(repeated_emails.length){
                            var repeated_str = repeated_emails.join(' - ');
                            valid = false;
                            alert('You are already registered under ' + repeated_str + ' for this event .. Maximum 1 registration per person is allowed.');
                        }
                        if(invalid_answers.length){
                            valid = false;
                            for(var k = 0 ; k < invalid_answers.length ; k++){
                                var options = answer_elem[invalid_answers[k]];
                                for(var m = 0; m < options.length ; m++){
                                    var option = options[m];
                                    $($(option).parent().next()).removeClass('o_hidden');
                                }
    //                            $($(option).parent()).after('<span="invalid-error" style="color:red;" class="invalid-answer">This Answer Disabled You To Continue.</span>');;
                            }
                        }

                    }
                    if(valid){
                        $(form).submit();
                    }
                });
            }
        }

    })

})