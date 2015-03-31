$('.btnact').click(function() {
  var fid = $(this).data('fid');
  var findex = $(this).data('findex');
  var papertitle=$(this).data('papertitle');
  var act = $(this).data('act');
  var Act = act[0].toUpperCase() + act.slice(1);
  var msg = Act + ' ' + findex + ' :"'+papertitle+'"';
  $('.modal-title').html(Act+' '+findex);
  if (act=="transfer"){
    var ss={'1':'1. Green mining and ecological mines (containing energy strategies)',
            '2':'2. Mine safety and occupational health',
            '3':'3. Geo-mechanics and geo-environmental engineering',
            '4':'4. Clean coal technology and low-carbon utilization',
            '5':'5. Intelligent mining equipment and technology',
            '6':'6. Exploitation of mineral resources and new energy (containing mineral economics)'};
    var s = $('<select id="to_s" class="form-control" name="to_session"/>');
    for(var val in ss){
      $('<option />', {value: val, text: ss[val]}).appendTo(s);
    };
    $('.modal-body').html(msg+' to</br>');
    s.appendTo($('.modal-body'));
  } else if (act=='modify'){
    var kk ={'Brief Abstract':'Brief Abstract',
             'Extended Abstract':'Extended Abstract',
             'Full Paper':'Full Paper'};
    var k = $('<select id="to_kind" class="form-control" name="to_session"/>');
    for (var val in kk){
      $('<option />', {value: val, text: kk[val]}).appendTo(k);
    };
    $('.modal-body').html(msg+' to</br>');
    k.appendTo($('.modal-body'));
  } else {
    $('.modal-body').html(msg+'?');
  }
  $('#actbtn').html(Act);
  $('#confirmModal').data('fid',fid).data('act',act);
  $('#confirmModal').modal('show');
});

$('#actbtn').click(function(){
  var fid =$('#confirmModal').data('fid');
  var act =$('#confirmModal').data('act');

  if (act=="transfer"){
    var to_s =$('#to_s').val();
    $.post(act,{fid:fid,to_s:to_s},function(res){
      if (res=="success"){
        $('#trline-'+fid).remove();
        $('#confirmModal').modal('hide');
      }
    });
  } else if (act == "modify"){
    var to_kind=$('#to_kind').val();
    $.post("modify_kind",{fid:fid,to_kind:to_kind},function(res){
      if(res=="success"){
        $('#trline-'+fid+">td:nth-child(3)").html(to_kind);
        $('#confirmModal').modal('hide');
      }
    });
  } else if (act=="accept") {
    $.post(act,{fid:fid},function(res){
      if (res=="success"){
        $('#trline-'+fid).removeClass("danger").removeClass('success');
        $('#trline-'+fid+">td:nth-child(4)").html('accepted');
        $('#confirmModal').modal('hide');
      }});
  } else if (act=="reject"){
    $.post(act,{fid:fid},function(res){
      if (res=="success"){
        $('#trline-'+fid).removeClass('success').addClass('danger');
        $('#trline-'+fid+">td:nth-child(4)").html('rejected');
        $('#confirmModal').modal('hide');
      }});
  } else if (act=="cancel"){
    $.post(act,{fid:fid},function(res){
      if (res=="success"){
        $('#trline-'+fid).remove();
        $('#confirmModal').modal('hide');
      }});
  }
});
