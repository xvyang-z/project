import {createBrowserRouter} from "react-router-dom";
import {MainPage, loader as rootLoader, action as rootAction} from "../views/index.jsx";
import {ErrorPage} from "../views/error.jsx";
import {Contact, loader as contactLoader, action as contactAction} from "../views/contact/index.jsx";
import {EditContact, action as editAction,} from "../views/contact/edit.jsx";
import {action as destroyAction} from "../views/contact/delete.jsx";

export const router = createBrowserRouter([
        {
            path: "/",
            element: <MainPage/>,
            errorElement: <ErrorPage/>,
            loader: rootLoader,
            action: rootAction,
            children: [
                {
                    errorElement: <ErrorPage/>,
                    children: [
                        {path: '', element: <p>default page</p>},
                        {
                            path: "contacts/:contactId",
                            element: <Contact/>,
                            loader: contactLoader,
                            action: contactAction
                        },
                        {
                            path: "contacts/:contactId/edit",
                            element: <EditContact/>,
                            loader: contactLoader,
                            action: editAction,
                        },
                        {
                            path: "contacts/:contactId/destroy",
                            action: destroyAction,
                        },
                    ]
                }
            ]
        },

    ])
;
