import "./Input.css"


function Input({title,placeholder,type,value,changeValue,id}) {
    return ( 
        

        <div className="i-g">

        <label htmlFor={id}>{title}</label>
        <input value={value} onChange={(e)=>changeValue(e.target.value)} id={id} placeholder={placeholder} type={type} />

        </div>
        
       
     );
}

export default Input;