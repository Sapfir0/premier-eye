const ClientRoutes = {
    NotFound: '/notFound',
    Forbidden: '/forbidden',
    BadGateway: '/badGateway',
    Index: '/home',
    Settings: '/settings',
    AreaMap: '/map',
    Logger: '/logger',
} as const;

export type ClientRouteType = typeof ClientRoutes[keyof typeof ClientRoutes];

export { ClientRoutes };

