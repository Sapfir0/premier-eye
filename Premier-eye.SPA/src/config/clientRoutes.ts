
const ClientRoutes = {
    Logout: "/logout",
    NotFound: "/notFound",
    Forbidden: "/forbidden",
    BadGateway: "/badGateway",
    Login: "/login",
    Index: "/"

} as const

export type ClientRouteType = typeof ClientRoutes[keyof typeof ClientRoutes]


export default ClientRoutes
