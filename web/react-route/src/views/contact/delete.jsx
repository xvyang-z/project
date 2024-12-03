import { redirect } from "react-router-dom";
import {deleteContact} from "../../api/contacts.js";


export async function action({ params }) {
    await deleteContact(params.contactId);
    return redirect("/");
}
