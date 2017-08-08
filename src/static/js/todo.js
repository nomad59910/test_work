// $(document).ready(function() {
//     var urlLoadTask = "/task/api/tasks-list?limit=5";
//     var isLoadind = false;
//
// 	var win = $(window);
//     LoadTask();
//
// 	win.scroll(function() {
// 		if ($(document).height() - win.height() == win.scrollTop() && !isLoadind) {
//             isLoadind = true;
//             LoadTask(urlLoadTask);
// 		}
// 	});
//
//     function getTask(url){
//         var resultData = undefined;
//         $.get({
//             type: "GET",
//             url: url,
//             success: function(data){
//                 resultData = data;
//             },
//             dataType: "JSON",
//             async: false,
//         });
//
//         return resultData;
//     }
//
//     function LoadTask(){
//         $('#loading').show();
//         if (!urlLoadTask) {
//             $('#loading').hide();
//             return;
//         }
//         var tasks = getTask(urlLoadTask);
//         urlLoadTask = tasks["next"]
//
//         var tmpl = document.getElementById('task-template').innerHTML;
//         var html = _.template(tmpl)({ items: tasks["results"] })
//
//         $('#tasks-content').append(html);
//         $('#loading').hide();
//         isLoadind = false;
//     }
// });

var urlLoadTask = "/task/api/tasks-list?limit=13";

function getTask(url){
    var resultData = undefined;
    $.get({
        type: "GET",
        url: url,
        success: function(data){
            resultData = data;
        },
        dataType: "JSON",
        async: false,
    });

    return resultData;
}


var Todos = Vue.extend({
    name: 'todos'
});

var vm = new Vue({
    delimiters: ["[", "]"],
    el : '#todos',
    data : {
        tasks : [],
        isLoadind : true,
        next: undefined,
        newTask:{
            "name": "",
            "description": "",
            "user_added": "admin",
            "date_created": '-',
            "is_done": false
        }
    },
    mounted : function(){
        var tasks = getTask(urlLoadTask);
        this.tasks = tasks["results"];
        this.next = tasks["next"];
        this.isLoadind = false;
    },
    created () {
        $(window).scroll(this.handleScroll);
    },
    methods: {
        addTask: function(){
            console.log(this.newTask);
            var newTask = Object.assign({}, this.newTask);
            this.tasks.unshift(newTask);
            this.newTask.name = "";
            this.newTask.description = "";
        },
        removeTask : function(index){
            this.tasks.splice(index, 1);
        },
        changeState : function(index){
            console.log(this.tasks[index]);
            this.tasks[index].is_done = !this.tasks[index].is_done;
        },
        handleScroll : function(e) {
    		if ($(document).height() - $(window).height() == $(window).scrollTop() && !this.isLoadind) {
                this.isLoadind = true;
                if (this.next) {
                    var tasks = getTask(this.next);
                    this.tasks = this.tasks.concat(tasks["results"]);
                    this.next = tasks["next"];
                    this.isLoadind = false;
                }
                else{
                    this.isLoadind = false;
                }
    		}
        }
    },
});
