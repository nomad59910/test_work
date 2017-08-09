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

Vue.component('modal', {
    template: '#modal-template',
    props: ['show'],
    data: function () {
        return {
            name: "",
            description: "",
        }
    },
    methods: {
        savePost: function () {
            this.$emit('save-data', this.name, this.description);
            this.close();
        },
        close: function () {
            this.$emit('hide-modal');
            this.name = "";
            this.description = "";
        }
    },
    mounted: function () {
        document.addEventListener("keydown", (e) => {
            if (this.show && e.keyCode == 27) {
                this.close();
            }
        });
    }
});

var vm = new Vue({
    delimiters: ["[", "]"],
    el : '#todos',
    data : {
        showModal: false,
        tasks : [],
        isLoadind : true,
        next: undefined,
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
        hideModal: function(){
            this.showModal = false;
        },
        addTask: function(name, description){
            console.log(this.newTask);
            var newTask = Object.assign({}, this.newTask);
            this.tasks.unshift({
                "name": name,
                "description": description,
                "user_added": "admin",
                "date_created": '-',
                "is_done": false
            });
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
