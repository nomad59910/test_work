var urlLoadTask = "/api/task/list/";

function getTask(url, params){
    var resultData = undefined;

    if (!params) {
        var params = {};
    }

    $.get({
        type: "GET",
        url: url,
        data: params,
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
            error: {
                name : '',
                description : '',
            }
        }
    },
    methods: {
        saveTask: function () {
            params = {
                "name": this.name,
                "description": this.description,
            }

            var that = this;
            $.post({
                dataType: 'json',
                url: '/api/task/add/',
                data: params,
                success: function(data){
                    that.$emit('save-data', data);
                    that.close();
                },
                error: function(error) {
                    errorJson = error.responseJSON;
                    for (var prop in errorJson) {
                        if(!errorJson.hasOwnProperty(prop)) continue;
                        that.error[prop] = errorJson[prop].join(' ');
                    }
                },
                dataType: "JSON",
                async: false,
            });
        },
        close: function () {
            this.$emit('hide-modal');
            this.name = "";
            this.description = "";
            this.error = {
                name : '',
                description : '',
            };
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
    props: ['show', 'task', 'title'],
    data: function () {
        return {
            name: "",
            description: "",
            error: {
                name : '',
                description : '',
            }
        }
    },
    methods: {
        saveTask: function () {
            var url = '/api/task/edit/' + this.task.id + '/'
            params = {
                name: this.name,
                description: this.description,
            }

            var that = this;
            $.ajax({
                type: "PUT",
                dataType: 'json',
                url: url,
                data: params,
                success: function(data){
                    that.$emit('save-data', data, that.task.id);
                    that.close();
                },
                error: function(error) {
                    errorJson = error.responseJSON;
                    for (var prop in errorJson) {
                        if(!errorJson.hasOwnProperty(prop)) continue;
                        that.error[prop] = errorJson[prop].join(' ');
                    }
                },
                dataType: "JSON",
                async: false,
            });
        },
        close: function () {
            this.$emit('hide-modal');
        }
    },
    watch : {
        show : function () {
            this.name = this.task.name;
            this.description = this.task.description;
            this.error = {
                name : '',
                description : '',
            };
        },
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
        editingTask: "",
        tasks : [],
        isLoadind : true,
        isFilter: false,
    },
    methods: {
        changeTask: function(data, id){
            var taskId = this.tasks.findIndex(task => task.id == id);
            for (var prop in data) {
                if(!data.hasOwnProperty(prop)) continue;
                this.tasks[taskId][prop] = data[prop]
            }
        },
        addTask: function(newTask){
            this.tasks.unshift(newTask);
        },
        removeTask : function(index){
            var idTask =  this.tasks[index].id
            var url =  '/api/task/delete/' + idTask + '/'
            var that = this;
            $.ajax({
                type: "DELETE",
                dataType: 'json',
                url: url,
                success: function(data){
                    that.tasks.splice(index, 1);
                },
                error: function(error) {
                    errorJson = error.responseJSON;
                    console.log(errorJson);
                },
                dataType: "JSON",
                async: false,
            });
        },
        changeState : function(index){
            var that = this;
            if (!this.tasks[index].is_done) {
                $.ajax({
                    type: "PUT",
                    dataType: 'json',
                    url: '/api/task/done/' + this.tasks[index].id + '/',
                    success: function(data){
                        that.tasks[index].is_done = data.is_done;
                    },
                    error: function(error) {
                        errorJson = error.responseJSON;
                        console.log(errorJson);
                    },
                    dataType: "JSON",
                    async: false,
                });
            }
            else{
                $.ajax({
                    type: "PUT",
                    dataType: 'json',
                    url: '/api/task/undone/' + this.tasks[index].id + '/',
                    success: function(data){
                        that.tasks[index].is_done = data.is_done;
                    },
                    error: function(error) {
                        errorJson = error.responseJSON;
                        console.log(errorJson);
                    },
                    dataType: "JSON",
                    async: false,
                });
            }
        },
        openChangeTaskModal: function(index){
            this.editingTask = this.tasks[index];
            this.showEditTaskModal = true;
        },
        handleScroll : function(e) {
    		if (($(document).height() - $(window).height()) - 20 < $(window).scrollTop() && !this.isLoadind) {
                this.isLoadind = true;

                var params = {}
                var params = {limit: 10}
                if (this.isFilter) params["done"] = "False";
                params["prev_id"] = this.tasks[this.tasks.length - 1].id;
                var tasks = getTask(urlLoadTask, params);

                this.tasks = this.tasks.concat(tasks);
                this.isLoadind = false;
    		}
        },
        loadTasks: function(){
            this.tasks = [];
            this.isLoadind = true;

            var params = {limit: 10}
            if (this.isFilter) params["done"] = "False";

            var tasks = getTask(urlLoadTask, params);

            this.tasks = tasks;
            this.isLoadind = false;
        },
    },
    mounted : function(){
        this.loadTasks();
    },
    created () {
        $(window).scroll(this.handleScroll);
    },
});
