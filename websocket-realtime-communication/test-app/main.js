class PageForm{
    get message(){ return document.querySelector("input[name=s_msg]") }
    get button(){ return document.querySelector(".s-btn") }
    get result(){ return document.querySelector(".result") }
}


class Page{
    constructor(){
        console.log("Page inited !!")
        this.ws = null
        this.form = new PageForm()
        
        this.connect_socket("ws://localhost:9001/")
    }

    connect_socket(url){
        let ws = new WebSocket(url)

        ws.addEventListener("open", () => {
            console.log("[!] Connection is open !!")
        })
        ws.addEventListener("message", (e) => {
            console.log("[!] new Message ", e.data)
            this.result = e.data
        })
        ws.addEventListener("error", () => {
            console.log("[!] Connection contains errors !!")
        })
        ws.addEventListener("close", () => {
            console.log("[!] Connection is closed !!")
        })
        
        this.ws = ws

        this.form.button.addEventListener("click", () => {
            this.send_message()
        })
    }

    send_message(){
        this.ws.send(this.query)
    }

    get query(){
        return this.form.message.value
    }

    set result(content){
        const result = this.form.result
        result.textContent = content
    }
}


function init(){
    const page = new Page();

}


window.onload = () => {
    init()
};