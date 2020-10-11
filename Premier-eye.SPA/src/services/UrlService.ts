import {createBrowserHistory} from "history";
import {injectable} from "inversify";
import {IUrlService} from "./typings/IUrlService";


@injectable()
class UrlService implements IUrlService {
    public history = createBrowserHistory()

    public redirect = (url: string): void => {
        this.history.push(url.toString())
    }

}

export default UrlService
