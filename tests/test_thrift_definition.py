# SPDX-FileCopyrightText: Copyright (c) 2026, NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
HEAVY_THRIFT = PROJECT_ROOT / "thrift_definition" / "heavy.thrift"


def test_heavy_thrift_tracks_post_distributed_contract():
    text = HEAVY_THRIFT.read_text(encoding="utf-8")

    removed_markers = [
        "enum TRole",
        "typedef string TKrb5Token",
        "typedef i64 TQueryId",
        "typedef i64 TSubqueryId",
        "struct TKrb5Session",
        "enum TMergeType",
        "struct TStepResult",
        "struct TPendingQuery",
        "struct TPendingRenderQuery",
        "struct TRenderStepResult",
        "struct TLicenseInfo",
        "  REPLICATED,",
        "struct TCreateParams",
        "bool is_replicated",
        "TCreateParams create_params",
        "AbstractDBObjectType = 0",
        "TRole role",
        "string host_id",
        "i32 leaf_index",
        "krb5_connect",
        "set_cur_session",
        "invalidate_cur_session",
        "set_leaf_info",
        "query_get_outer_fragment_count",
        "start_query",
        "execute_query_step",
        "broadcast_serialized_rows",
        "start_render_query",
        "execute_next_render_step",
        "insert_data",
        "insert_chunks",
        "checkpoint",
        "set_license_key",
        "get_license_claims",
    ]
    for marker in removed_markers:
        assert marker not in text

    current_markers = [
        "struct TServerStatus",
        "9: string renderer_status_json",
        "3: string immerse_metadata_json",
        "44: string bounding_box_clip",
        "struct TColumnPermissions",
        "  SHARDED = 2,",
        "AbstractDBObjectType,",
        "void create_table(1: TSessionId session, 2: string table_name, 3: TRowDescriptor row_desc) throws",
        "void import_geo_table(1: TSessionId session, 2: string table_name, 3: string file_name, 4: TCopyParams copy_params, 5: TRowDescriptor row_desc) throws",
        "6: TColumnPermissions column_permissions_",
        "ColumnDBObjectType",
        "put_immerse_users_metadata",
        "put_immerse_database_metadata",
        "list<TUserInfo> get_users_info",
        "list<TDBInfo> get_databases",
    ]
    for marker in current_markers:
        assert marker in text

