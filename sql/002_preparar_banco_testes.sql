-- Executar conectado a foodagent_test como postgres.
-- O banco foodagent_test e o usuario foodagent_app devem existir.
-- Nao contem senhas. Pode ser reaplicado sem apagar registros.
BEGIN;

DO $$
BEGIN
    IF current_database() <> 'foodagent_test' THEN
        RAISE EXCEPTION 'Execute somente no banco foodagent_test.';
    END IF;
END;
$$;

GRANT CONNECT ON DATABASE foodagent_test TO foodagent_app;
GRANT USAGE ON SCHEMA public TO foodagent_app;

CREATE TABLE IF NOT EXISTS public.pedidos (
    id VARCHAR(7) PRIMARY KEY,
    status VARCHAR(20) NOT NULL,
    criado_em TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT pedido_id_formato CHECK (id ~ '^PED-[0-9]{3}$'),
    CONSTRAINT pedido_status_valido
        CHECK (status IN ('em preparo', 'em entrega', 'entregue'))
);

INSERT INTO public.pedidos (id, status)
VALUES ('PED-901', 'em preparo'), ('PED-902', 'entregue')
ON CONFLICT (id) DO NOTHING;

GRANT SELECT ON TABLE public.pedidos TO foodagent_app;
COMMIT;
