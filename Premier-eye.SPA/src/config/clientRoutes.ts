
const ClientRoutes = {
    Logout: "/logout",
    NotFound: "/notFound",
    Forbidden: "/forbidden",
    BadGateway: "/badGateway",
    Login: "/login",
    Index: "/",
    Settings: '/settings'

} as const

export type ClientRouteType = typeof ClientRoutes[keyof typeof ClientRoutes]


export {ClientRoutes}
