$(".del").on('click',function(){
	var file_name= $(this).parent().parent().children('.file_name').children().text();
	var r=confirm("是否删除？");
	if (r==true)
	{
		 $.ajax({
            url: '/delete/'+file_name,
            type: 'GET',
            dataType: 'json'
        })
        .done(function(data) {
			if(data.status=='1'){
				alert('删除成功');
				location.reload();// = location;
			}else{
				alert('删除失败');
			}
        })
	}
})
