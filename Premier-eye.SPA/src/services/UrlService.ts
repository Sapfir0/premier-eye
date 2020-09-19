import {createBrowserHistory} from "history";
import {injectable} from "inversify";
import {IUrlService} from "./typings/IUrlService";


@injectable()
class UrlService implements IUrlService {
    public history = createBrowserHistory({
        getUserConfirmation: (message, callback) => callback(window.confirm(message))
    })

    public redirect = (url: string): void => {
        this.history.push(url.toString())
    }

}

export default UrlService
