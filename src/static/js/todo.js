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

Vue.component('add-task-modal', {
    delimiters: ["[", "]"],
    template: '#modal-template',
    props: ['show', 'title'],
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

Vue.component('edit-task-modal', {
    delimiters: ["[", "]"],
    template: '#modal-template',
    props: ['show', 'name_', 'description_', 'title'],
    data: function () {
        return {
            name: this.name_,
            description: this.description_,
        }
    },
    methods: {
        savePost: function () {
            this.$emit('save-data', {   });
            this.close();
        },
        close: function () {
            this.$emit('hide-modal');
        }
    },
    watch : {
        name_ : function () {
            this.name = this.name_;
        },
        description_ : function () {
            this.description = this.description_;
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
        showAddTaskModal: false,
        showEditTaskModal: false,
        editingTaskName: "",
        editingTaskDescription: "",
        tasks : [],
        isLoadind : true,
        next: undefined,
    },
    methods: {
        changeTask: function(data){
            // this.tasks[this.editingTaskId].name = name;
            // this.tasks[this.editingTaskId].description = description;
        },
        addTask: function(name, description){
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
            this.tasks[index].is_done = !this.tasks[index].is_done;
        },
        openChangeTaskModal: function(index){
            this.editingTaskName = this.tasks[index].name;
            this.editingTaskDescription = this.tasks[index].description;
            this.showEditTaskModal = true;
        },
        handleScroll : function(e) {
    		if (($(document).height() - $(window).height()) - 20 < $(window).scrollTop() && !this.isLoadind) {
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
    mounted : function(){
        var tasks = getTask(urlLoadTask);
        this.tasks = tasks["results"];
        this.next = tasks["next"];
        this.isLoadind = false;
    },
    created () {
        $(window).scroll(this.handleScroll);
    },
});
