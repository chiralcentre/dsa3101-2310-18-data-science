import { useRef } from "react";
import emailjs from '@emailjs/browser';

const Feedback = () => {
    const form = useRef();

    const sendEmail = (e) => {
        e.preventDefault();

        emailjs.sendForm(
            'service_azyfm6r', 'template_3pb3hsk', form.current, '7GvpV8WfeZHYqsB6T')
            .then((result) => {
                console.log(result.text);
                alert("Your message has been sent. Thank you for your feedback.")

                // Clear the form after successful submisssion 
                form.current.reset();
            }, (error) => {
                console.log(error.text);
                alert("Failed. Please try again later.", error)
            });
    };

    return (
        <div className="container-feedback">
            <div className="feedback">
                <div className="feedback-text-box">
                    <h2 className="feedback-text">Get in touch with us!</h2>
                    <p className="feedback-text subtitle">
                        Whether you have a question or just want to leave us some feedbacks, we would like to hear from you! Please fill out the form below and we'll get back to you as soon as possible.
                    </p>

                    <form ref={form} className="feedback-form" onSubmit={sendEmail}>
                        <div>
                            <label for="name">Name</label>
                            <input
                                id="name"
                                type="name"
                                placeholder="Jonas Ho"
                                name="name"
                                required
                            />
                        </div>

                        <div>
                            <label for="email">Email address</label>
                            <input
                                id="email"
                                type="email"
                                placeholder="jonasho@example.com"
                                name="email"
                                required
                            />
                        </div>

                        <div>
                            <label for="subject">Subject</label>
                            <input
                                id="subject"
                                type="subject"
                                placeholder="Feedbacks for Data Guru"
                                name="subject"
                                required
                            />
                        </div>

                        <div>
                            <label for="message">Message</label>
                            <textarea id="message" name="message" placeholder="Write your message here"></textarea>

                        </div>

                        <button type="submit" className="btn btn--form">Submit</button>
                    </form>

                </div>
            </div>
        </div>
    );
}

export default Feedback;