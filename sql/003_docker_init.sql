CREATE TABLE IF NOT EXISTS public.pedidos (
    id VARCHAR(7) PRIMARY KEY,
    status VARCHAR(20) NOT NULL,
    criado_em TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT pedido_id_formato CHECK (id ~ '^PED-[0-9]{3}$'),
    CONSTRAINT pedido_status_valido
        CHECK (status IN ('em preparo', 'em entrega', 'entregue'))
);

INSERT INTO public.pedidos (id, status)
VALUES ('PED-001', 'em preparo'), ('PED-002', 'entregue')
ON CONFLICT (id) DO NOTHING;
