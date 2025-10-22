import { useState } from "react";
import api from "./api";

type Customer = {
    firstName: string;
    lastName: string;
    email: string;
};

export default function CustomerForm(){
    const [customer, setCustomer] = useState<Customer>({
        firstName: "",
        lastName: "",
        email: "",
    });
    const [loading, setLoading] = useState(false);
    const [err, setErr] = useState<string | null>(null);

    function handleChange(e: React.ChangeEvent<HTMLInputElement>) {
        setCustomer({
            ...customer,
            [e.target.name]: e.target.value
        });
    }

    const addCustomer = async (c : Customer) => {
        try {
            await api.post('/customers', {first_name: c.firstName, last_name: c.lastName, email: c.email, preferred_lang: "en"})
        } catch (error) {
            console.error("Error adding customer")
        }
    }

    async function handleSubmit() {
        setLoading(true);
        setErr(null);
        await addCustomer(customer);
        setLoading(false);
    }

    return (
        <div>
        <form className="form" onSubmit={handleSubmit}>
        <label className="field"> First Name:
            <input name="firstName" value={customer.firstName} onChange={handleChange} />
        </label>
        <label className="field"> Last Name:
            <input name="lastName" value={customer.lastName} onChange={handleChange} />
        </label>
        <label className="field"> Email:
            <input name="email" value={customer.email} onChange={handleChange} />
        </label>
        <button type="submit" disabled={customer.firstName.length === 0 || customer.lastName.length === 0 || customer.email.length === 0 || loading}> Submit </button>
        </form>

        {loading && <p>Loading</p>}
        </div>
    );

}