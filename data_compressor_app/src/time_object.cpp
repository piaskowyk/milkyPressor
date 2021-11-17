#include <assert.h>
#include <stdbool.h>

#include <anjay/anjay.h>
#include <anjay/lwm2m_send.h>
#include <avsystem/commons/avs_defs.h>
#include <avsystem/commons/avs_list.h>
#include <avsystem/commons/avs_log.h>
#include <avsystem/commons/avs_memory.h>

static void send_finished_handler(anjay_t *anjay,
                                anjay_ssid_t ssid,
                                const anjay_send_batch_t *batch,
                                int result,
                                void *data) {
    (void) anjay;
    (void) ssid;
    (void) batch;
    (void) data;

    if (result != ANJAY_SEND_SUCCESS) {
        avs_log(time_object, ERROR, "Send failed, result: %d", result);
    } else {
        avs_log(time_object, TRACE, "Send successful");
    }
}

void time_object_send(anjay_t *anjay, const anjay_dm_object_def_t **def) {
    if (!anjay || !def) {
        return;
    }
    time_object_t *obj = get_obj(def);
    const anjay_ssid_t server_ssid = 1;

    // Allocate new batch builder.
    anjay_send_batch_builder_t *builder = anjay_send_batch_builder_new();

    if (!builder) {
        avs_log(time_object, ERROR, "Failed to allocate batch builder");
        return;
    }

    int res = 0;

    AVS_LIST(time_instance_t) it;
    AVS_LIST_FOREACH(it, obj->instances) {
        // Add current values of resources from Time Object.
        if (anjay_send_batch_data_add_current(builder, anjay, obj->def->oid,
                                            it->iid, RID_CURRENT_TIME)
                || anjay_send_batch_data_add_current(builder, anjay,
                                                    obj->def->oid, it->iid,
                                                    RID_APPLICATION_TYPE)) {
            anjay_send_batch_builder_cleanup(&builder);
            avs_log(time_object, ERROR, "Failed to add batch data, result: %d",
                    res);
            return;
        }
    }
    // After adding all values, compile our batch for sending.
    anjay_send_batch_t *batch = anjay_send_batch_builder_compile(&builder);

    if (!batch) {
        anjay_send_batch_builder_cleanup(&builder);
        avs_log(time_object, ERROR, "Batch compile failed");
        return;
    }

    // Schedule our send to be run on next `anjay_sched_run()` call.
    res = anjay_send(anjay, server_ssid, batch, send_finished_handler, NULL);

    if (res) {
        avs_log(time_object, ERROR, "Failed to send, result: %d", res);
    }

    // After scheduling, we can release our batch.
    anjay_send_batch_release(&batch);
}