import "./Button.css"
import {Link} from "react-router-dom"

export function Button({to,text}) {
    return ( 
    
   <Link className="universal_button" to={to}>

        <button>{text}</button>

   </Link>
    
    );
}


export function StaticButton({onclick,text}) {
    return ( 
    
        <span className="universal_button">
        <button onClick={onclick}>{text}</button>
        </span>
   
    
    );
}
