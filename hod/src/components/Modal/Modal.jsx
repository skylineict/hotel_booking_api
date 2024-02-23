import "./Modal.css"


function Modal({ isOpen, onClose, children }) {
    return ( 

        <>


        {isOpen && (

        <div className="modal-overlay">
        <div className="modal-content">

            <div className="modal-top">
               <button className="modal-close" onClick={onClose}>
            &times;
            </button> 
            </div>

            <div className="modal-body">

               {children}

            </div>
            
           
        </div>
        </div>

        )}

        

    </>
     );
}

export default Modal;