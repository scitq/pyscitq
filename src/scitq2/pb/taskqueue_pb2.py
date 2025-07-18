# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: taskqueue.proto
# Protobuf Python Version: 6.31.0
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC,
    6,
    31,
    0,
    '',
    'taskqueue.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0ftaskqueue.proto\x12\ttaskqueue\x1a\x1bgoogle/protobuf/empty.proto\"\x1f\n\x0cTaskResponse\x12\x0f\n\x07task_id\x18\x01 \x01(\r\"D\n\nWorkerInfo\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x18\n\x0b\x63oncurrency\x18\x02 \x01(\rH\x00\x88\x01\x01\x42\x0e\n\x0c_concurrency\"\xb2\x04\n\x0bTaskRequest\x12\x0f\n\x07\x63ommand\x18\x01 \x01(\t\x12\x12\n\x05shell\x18\x02 \x01(\tH\x00\x88\x01\x01\x12\x11\n\tcontainer\x18\x03 \x01(\t\x12\x1e\n\x11\x63ontainer_options\x18\x04 \x01(\tH\x01\x88\x01\x01\x12\x14\n\x07step_id\x18\x05 \x01(\rH\x02\x88\x01\x01\x12\r\n\x05input\x18\x06 \x03(\t\x12\x10\n\x08resource\x18\x07 \x03(\t\x12\x13\n\x06output\x18\x08 \x01(\tH\x03\x88\x01\x01\x12\x12\n\x05retry\x18\t \x01(\rH\x04\x88\x01\x01\x12\x15\n\x08is_final\x18\n \x01(\x08H\x05\x88\x01\x01\x12\x17\n\nuses_cache\x18\x0b \x01(\x08H\x06\x88\x01\x01\x12\x1d\n\x10\x64ownload_timeout\x18\x0c \x01(\x02H\x07\x88\x01\x01\x12\x1c\n\x0frunning_timeout\x18\r \x01(\x02H\x08\x88\x01\x01\x12\x1b\n\x0eupload_timeout\x18\x0e \x01(\x02H\t\x88\x01\x01\x12\x0e\n\x06status\x18\x0f \x01(\t\x12\x12\n\ndependency\x18\x10 \x03(\r\x12\x16\n\ttask_name\x18\x11 \x01(\tH\n\x88\x01\x01\x42\x08\n\x06_shellB\x14\n\x12_container_optionsB\n\n\x08_step_idB\t\n\x07_outputB\x08\n\x06_retryB\x0b\n\t_is_finalB\r\n\x0b_uses_cacheB\x13\n\x11_download_timeoutB\x12\n\x10_running_timeoutB\x11\n\x0f_upload_timeoutB\x0c\n\n_task_name\"\xf8\x04\n\x04Task\x12\x0f\n\x07task_id\x18\x01 \x01(\r\x12\x0f\n\x07\x63ommand\x18\x02 \x01(\t\x12\x12\n\x05shell\x18\x03 \x01(\tH\x00\x88\x01\x01\x12\x11\n\tcontainer\x18\x04 \x01(\t\x12\x1e\n\x11\x63ontainer_options\x18\x05 \x01(\tH\x01\x88\x01\x01\x12\x14\n\x07step_id\x18\x06 \x01(\rH\x02\x88\x01\x01\x12\r\n\x05input\x18\x07 \x03(\t\x12\x10\n\x08resource\x18\x08 \x03(\t\x12\x13\n\x06output\x18\t \x01(\tH\x03\x88\x01\x01\x12\x12\n\x05retry\x18\n \x01(\rH\x04\x88\x01\x01\x12\x15\n\x08is_final\x18\x0b \x01(\x08H\x05\x88\x01\x01\x12\x17\n\nuses_cache\x18\x0c \x01(\x08H\x06\x88\x01\x01\x12\x1d\n\x10\x64ownload_timeout\x18\r \x01(\x02H\x07\x88\x01\x01\x12\x1c\n\x0frunning_timeout\x18\x0e \x01(\x02H\x08\x88\x01\x01\x12\x1b\n\x0eupload_timeout\x18\x0f \x01(\x02H\t\x88\x01\x01\x12\x0e\n\x06status\x18\x10 \x01(\t\x12\x16\n\tworker_id\x18\x11 \x01(\rH\n\x88\x01\x01\x12\x18\n\x0bworkflow_id\x18\x12 \x01(\rH\x0b\x88\x01\x01\x12\x16\n\ttask_name\x18\x13 \x01(\tH\x0c\x88\x01\x01\x42\x08\n\x06_shellB\x14\n\x12_container_optionsB\n\n\x08_step_idB\t\n\x07_outputB\x08\n\x06_retryB\x0b\n\t_is_finalB\r\n\x0b_uses_cacheB\x13\n\x11_download_timeoutB\x12\n\x10_running_timeoutB\x11\n\x0f_upload_timeoutB\x0c\n\n_worker_idB\x0e\n\x0c_workflow_idB\x0c\n\n_task_name\"*\n\x08TaskList\x12\x1e\n\x05tasks\x18\x01 \x03(\x0b\x32\x0f.taskqueue.Task\"\xae\x01\n\x06Worker\x12\x11\n\tworker_id\x18\x01 \x01(\r\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\x13\n\x0b\x63oncurrency\x18\x03 \x01(\r\x12\x10\n\x08prefetch\x18\x04 \x01(\r\x12\x0e\n\x06status\x18\x05 \x01(\t\x12\x0c\n\x04ipv4\x18\x06 \x01(\t\x12\x0c\n\x04ipv6\x18\x07 \x01(\t\x12\x0e\n\x06\x66lavor\x18\x08 \x01(\t\x12\x10\n\x08provider\x18\t \x01(\t\x12\x0e\n\x06region\x18\n \x01(\t\"1\n\x0bWorkersList\x12\"\n\x07workers\x18\x01 \x03(\x0b\x32\x11.taskqueue.Worker\"\x14\n\x12ListWorkersRequest\"\x1c\n\nTaskUpdate\x12\x0e\n\x06weight\x18\x01 \x01(\x01\"\x90\x01\n\x0eTaskUpdateList\x12\x37\n\x07updates\x18\x01 \x03(\x0b\x32&.taskqueue.TaskUpdateList.UpdatesEntry\x1a\x45\n\x0cUpdatesEntry\x12\x0b\n\x03key\x18\x01 \x01(\r\x12$\n\x05value\x18\x02 \x01(\x0b\x32\x15.taskqueue.TaskUpdate:\x02\x38\x01\"\x89\x01\n\x10TaskListAndOther\x12\x1e\n\x05tasks\x18\x01 \x03(\x0b\x32\x0f.taskqueue.Task\x12\x13\n\x0b\x63oncurrency\x18\x02 \x01(\r\x12*\n\x07updates\x18\x03 \x01(\x0b\x32\x19.taskqueue.TaskUpdateList\x12\x14\n\x0c\x61\x63tive_tasks\x18\x04 \x03(\r\"7\n\x10TaskStatusUpdate\x12\x0f\n\x07task_id\x18\x01 \x01(\r\x12\x12\n\nnew_status\x18\x02 \x01(\t\">\n\x07TaskLog\x12\x0f\n\x07task_id\x18\x01 \x01(\r\x12\x10\n\x08log_type\x18\x02 \x01(\t\x12\x10\n\x08log_text\x18\x03 \x01(\t\"\x82\x01\n\x0eGetLogsRequest\x12\x0f\n\x07taskIds\x18\x01 \x03(\r\x12\x11\n\tchunkSize\x18\x02 \x01(\r\x12\x18\n\x0bskipFromEnd\x18\x03 \x01(\rH\x00\x88\x01\x01\x12\x15\n\x08log_type\x18\x04 \x01(\tH\x01\x88\x01\x01\x42\x0e\n\x0c_skipFromEndB\x0b\n\t_log_type\":\n\x08LogChunk\x12\x0e\n\x06taskId\x18\x01 \x01(\r\x12\x0e\n\x06stdout\x18\x02 \x03(\t\x12\x0e\n\x06stderr\x18\x03 \x03(\t\"1\n\x0cLogChunkList\x12!\n\x04logs\x18\x01 \x03(\x0b\x32\x13.taskqueue.LogChunk\"\x1b\n\x07TaskIds\x12\x10\n\x08task_ids\x18\x01 \x03(\r\"\x19\n\x06TaskId\x12\x0f\n\x07task_id\x18\x01 \x01(\r\"\x1d\n\x08WorkerId\x12\x11\n\tworker_id\x18\x01 \x01(\r\")\n\x13WorkerStatusRequest\x12\x12\n\nworker_ids\x18\x01 \x03(\r\"1\n\x0cWorkerStatus\x12\x11\n\tworker_id\x18\x01 \x01(\r\x12\x0e\n\x06status\x18\x02 \x01(\t\"A\n\x14WorkerStatusResponse\x12)\n\x08statuses\x18\x01 \x03(\x0b\x32\x17.taskqueue.WorkerStatus\"G\n\rWorkerDetails\x12\x11\n\tworker_id\x18\x01 \x01(\r\x12\x13\n\x0bworker_name\x18\x02 \x01(\t\x12\x0e\n\x06job_id\x18\x03 \x01(\r\">\n\tWorkerIds\x12\x31\n\x0fworkers_details\x18\x01 \x03(\x0b\x32\x18.taskqueue.WorkerDetails\"U\n\x19PingAndGetNewTasksRequest\x12\x11\n\tworker_id\x18\x01 \x01(\r\x12%\n\x05stats\x18\x02 \x01(\x0b\x32\x16.taskqueue.WorkerStats\"\x16\n\x03\x41\x63k\x12\x0f\n\x07success\x18\x01 \x01(\x08\"t\n\x10ListTasksRequest\x12\x1a\n\rstatus_filter\x18\x01 \x01(\tH\x00\x88\x01\x01\x12\x1d\n\x10worker_id_filter\x18\x02 \x01(\rH\x01\x88\x01\x01\x42\x10\n\x0e_status_filterB\x13\n\x11_worker_id_filter\"\xa3\x01\n\rWorkerRequest\x12\x13\n\x0bprovider_id\x18\x01 \x01(\r\x12\x11\n\tflavor_id\x18\x02 \x01(\r\x12\x11\n\tregion_id\x18\x03 \x01(\r\x12\x0e\n\x06number\x18\x04 \x01(\r\x12\x13\n\x0b\x63oncurrency\x18\x05 \x01(\r\x12\x10\n\x08prefetch\x18\x06 \x01(\r\x12\x14\n\x07step_id\x18\x07 \x01(\rH\x00\x88\x01\x01\x42\n\n\x08_step_id\"\x8e\x02\n\x13WorkerUpdateRequest\x12\x11\n\tworker_id\x18\x01 \x01(\r\x12\x18\n\x0bprovider_id\x18\x02 \x01(\rH\x00\x88\x01\x01\x12\x16\n\tflavor_id\x18\x03 \x01(\rH\x01\x88\x01\x01\x12\x16\n\tregion_id\x18\x04 \x01(\rH\x02\x88\x01\x01\x12\x18\n\x0b\x63oncurrency\x18\x05 \x01(\rH\x03\x88\x01\x01\x12\x15\n\x08prefetch\x18\x06 \x01(\rH\x04\x88\x01\x01\x12\x14\n\x07step_id\x18\x07 \x01(\rH\x05\x88\x01\x01\x42\x0e\n\x0c_provider_idB\x0c\n\n_flavor_idB\x0c\n\n_region_idB\x0e\n\x0c_concurrencyB\x0b\n\t_prefetchB\n\n\x08_step_id\"3\n\x12ListFlavorsRequest\x12\r\n\x05limit\x18\x01 \x01(\r\x12\x0e\n\x06\x66ilter\x18\x02 \x01(\t\"\x9c\x02\n\x06\x46lavor\x12\x11\n\tflavor_id\x18\x01 \x01(\r\x12\x13\n\x0b\x66lavor_name\x18\x02 \x01(\t\x12\x13\n\x0bprovider_id\x18\x03 \x01(\r\x12\x10\n\x08provider\x18\x04 \x01(\t\x12\x0b\n\x03\x63pu\x18\x05 \x01(\x05\x12\x0b\n\x03mem\x18\x06 \x01(\x02\x12\x0c\n\x04\x64isk\x18\x07 \x01(\x02\x12\x11\n\tbandwidth\x18\x08 \x01(\x05\x12\x0b\n\x03gpu\x18\t \x01(\t\x12\x0e\n\x06gpumem\x18\n \x01(\x05\x12\x0f\n\x07has_gpu\x18\x0b \x01(\x08\x12\x17\n\x0fhas_quick_disks\x18\x0c \x01(\x08\x12\x11\n\tregion_id\x18\r \x01(\r\x12\x0e\n\x06region\x18\x0e \x01(\t\x12\x10\n\x08\x65viction\x18\x0f \x01(\x02\x12\x0c\n\x04\x63ost\x18\x10 \x01(\x02\"1\n\x0b\x46lavorsList\x12\"\n\x07\x66lavors\x18\x01 \x03(\x0b\x32\x11.taskqueue.Flavor\"\x11\n\x0fListJobsRequest\"\xb5\x01\n\x03Job\x12\x0e\n\x06job_id\x18\x01 \x01(\r\x12\x0e\n\x06status\x18\x02 \x01(\t\x12\x11\n\tflavor_id\x18\x03 \x01(\r\x12\r\n\x05retry\x18\x04 \x01(\r\x12\x11\n\tworker_id\x18\x05 \x01(\r\x12\x0e\n\x06\x61\x63tion\x18\x06 \x01(\t\x12\x12\n\ncreated_at\x18\x07 \x01(\t\x12\x13\n\x0bmodified_at\x18\x08 \x01(\t\x12\x13\n\x0bprogression\x18\t \x01(\r\x12\x0b\n\x03log\x18\n \x01(\t\"\x17\n\x05JobId\x12\x0e\n\x06job_id\x18\x01 \x01(\r\"(\n\x08JobsList\x12\x1c\n\x04jobs\x18\x01 \x03(\x0b\x32\x0e.taskqueue.Job\"#\n\x10JobStatusRequest\x12\x0f\n\x07job_ids\x18\x01 \x03(\r\"@\n\tJobStatus\x12\x0e\n\x06job_id\x18\x01 \x01(\r\x12\x0e\n\x06status\x18\x02 \x01(\t\x12\x13\n\x0bprogression\x18\x03 \x01(\r\";\n\x11JobStatusResponse\x12&\n\x08statuses\x18\x01 \x03(\x0b\x32\x14.taskqueue.JobStatus\"\x1e\n\x0cRcloneConfig\x12\x0e\n\x06\x63onfig\x18\x01 \x01(\t\"2\n\x0cLoginRequest\x12\x10\n\x08username\x18\x01 \x01(\t\x12\x10\n\x08password\x18\x02 \x01(\t\"\x1e\n\rLoginResponse\x12\r\n\x05token\x18\x01 \x01(\t\"\x16\n\x05Token\x12\r\n\x05token\x18\x01 \x01(\t\"X\n\x11\x43reateUserRequest\x12\x10\n\x08username\x18\x01 \x01(\t\x12\x10\n\x08password\x18\x02 \x01(\t\x12\r\n\x05\x65mail\x18\x03 \x01(\t\x12\x10\n\x08is_admin\x18\x04 \x01(\x08\"\x19\n\x06UserId\x12\x0f\n\x07user_id\x18\x01 \x01(\r\"}\n\x04User\x12\x0f\n\x07user_id\x18\x01 \x01(\r\x12\x15\n\x08username\x18\x02 \x01(\tH\x00\x88\x01\x01\x12\x12\n\x05\x65mail\x18\x03 \x01(\tH\x01\x88\x01\x01\x12\x15\n\x08is_admin\x18\x04 \x01(\x08H\x02\x88\x01\x01\x42\x0b\n\t_usernameB\x08\n\x06_emailB\x0b\n\t_is_admin\"+\n\tUsersList\x12\x1e\n\x05users\x18\x01 \x03(\x0b\x32\x0f.taskqueue.User\"U\n\x15\x43hangePasswordRequest\x12\x10\n\x08username\x18\x01 \x01(\t\x12\x14\n\x0cold_password\x18\x02 \x01(\t\x12\x14\n\x0cnew_password\x18\x03 \x01(\t\"3\n\x0fRecruiterFilter\x12\x14\n\x07step_id\x18\x01 \x01(\rH\x00\x88\x01\x01\x42\n\n\x08_step_id\",\n\x0bRecruiterId\x12\x0f\n\x07step_id\x18\x01 \x01(\r\x12\x0c\n\x04rank\x18\x02 \x01(\r\"\xb1\x01\n\tRecruiter\x12\x0f\n\x07step_id\x18\x01 \x01(\r\x12\x0c\n\x04rank\x18\x02 \x01(\r\x12\x13\n\x0bprotofilter\x18\x03 \x01(\t\x12\x13\n\x0b\x63oncurrency\x18\x04 \x01(\r\x12\x10\n\x08prefetch\x18\x05 \x01(\r\x12\x18\n\x0bmax_workers\x18\x06 \x01(\rH\x00\x88\x01\x01\x12\x0e\n\x06rounds\x18\x07 \x01(\r\x12\x0f\n\x07timeout\x18\x08 \x01(\rB\x0e\n\x0c_max_workers\"\x94\x02\n\x0fRecruiterUpdate\x12\x0f\n\x07step_id\x18\x01 \x01(\r\x12\x0c\n\x04rank\x18\x02 \x01(\r\x12\x18\n\x0bprotofilter\x18\x03 \x01(\tH\x00\x88\x01\x01\x12\x18\n\x0b\x63oncurrency\x18\x04 \x01(\rH\x01\x88\x01\x01\x12\x15\n\x08prefetch\x18\x05 \x01(\rH\x02\x88\x01\x01\x12\x18\n\x0bmax_workers\x18\x06 \x01(\rH\x03\x88\x01\x01\x12\x13\n\x06rounds\x18\x07 \x01(\rH\x04\x88\x01\x01\x12\x14\n\x07timeout\x18\x08 \x01(\rH\x05\x88\x01\x01\x42\x0e\n\x0c_protofilterB\x0e\n\x0c_concurrencyB\x0b\n\t_prefetchB\x0e\n\x0c_max_workersB\t\n\x07_roundsB\n\n\x08_timeout\"9\n\rRecruiterList\x12(\n\nrecruiters\x18\x01 \x03(\x0b\x32\x14.taskqueue.Recruiter\"6\n\x0eWorkflowFilter\x12\x16\n\tname_like\x18\x01 \x01(\tH\x00\x88\x01\x01\x42\x0c\n\n_name_like\"!\n\nWorkflowId\x12\x13\n\x0bworkflow_id\x18\x01 \x01(\r\"u\n\x08Workflow\x12\x13\n\x0bworkflow_id\x18\x01 \x01(\r\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\x14\n\x0crun_strategy\x18\x04 \x01(\t\x12\x1c\n\x0fmaximum_workers\x18\x05 \x01(\rH\x00\x88\x01\x01\x42\x12\n\x10_maximum_workers\"}\n\x0fWorkflowRequest\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x19\n\x0crun_strategy\x18\x02 \x01(\tH\x00\x88\x01\x01\x12\x1c\n\x0fmaximum_workers\x18\x03 \x01(\rH\x01\x88\x01\x01\x42\x0f\n\r_run_strategyB\x12\n\x10_maximum_workers\"6\n\x0cWorkflowList\x12&\n\tworkflows\x18\x01 \x03(\x0b\x32\x13.taskqueue.Workflow\"\x19\n\x06StepId\x12\x0f\n\x07step_id\x18\x01 \x01(\r\"Q\n\x04Step\x12\x0f\n\x07step_id\x18\x01 \x01(\r\x12\x15\n\rworkflow_name\x18\x02 \x01(\t\x12\x13\n\x0bworkflow_id\x18\x03 \x01(\r\x12\x0c\n\x04name\x18\x04 \x01(\t\"s\n\x0bStepRequest\x12\x1a\n\rworkflow_name\x18\x01 \x01(\tH\x00\x88\x01\x01\x12\x18\n\x0bworkflow_id\x18\x02 \x01(\rH\x01\x88\x01\x01\x12\x0c\n\x04name\x18\x03 \x01(\tB\x10\n\x0e_workflow_nameB\x0e\n\x0c_workflow_id\"*\n\x08StepList\x12\x1e\n\x05steps\x18\x01 \x03(\x0b\x32\x0f.taskqueue.Step\"\xe3\x01\n\x0bWorkerStats\x12\x19\n\x11\x63pu_usage_percent\x18\x01 \x01(\x02\x12\x19\n\x11mem_usage_percent\x18\x02 \x01(\x02\x12\x11\n\tload_1min\x18\x03 \x01(\x02\x12\x16\n\x0eiowait_percent\x18\x04 \x01(\x02\x12#\n\x05\x64isks\x18\x05 \x03(\x0b\x32\x14.taskqueue.DiskUsage\x12\'\n\x07\x64isk_io\x18\x06 \x01(\x0b\x32\x16.taskqueue.DiskIOStats\x12%\n\x06net_io\x18\x07 \x01(\x0b\x32\x15.taskqueue.NetIOStats\"7\n\tDiskUsage\x12\x13\n\x0b\x64\x65vice_name\x18\x01 \x01(\t\x12\x15\n\rusage_percent\x18\x02 \x01(\x02\"u\n\x0b\x44iskIOStats\x12\x18\n\x10read_bytes_total\x18\x01 \x01(\x03\x12\x19\n\x11write_bytes_total\x18\x02 \x01(\x03\x12\x17\n\x0fread_bytes_rate\x18\x03 \x01(\x02\x12\x18\n\x10write_bytes_rate\x18\x04 \x01(\x02\"r\n\nNetIOStats\x12\x18\n\x10recv_bytes_total\x18\x01 \x01(\x03\x12\x18\n\x10sent_bytes_total\x18\x02 \x01(\x03\x12\x17\n\x0frecv_bytes_rate\x18\x03 \x01(\x02\x12\x17\n\x0fsent_bytes_rate\x18\x04 \x01(\x02\"+\n\x15GetWorkerStatsRequest\x12\x12\n\nworker_ids\x18\x01 \x03(\r\"\xae\x01\n\x16GetWorkerStatsResponse\x12H\n\x0cworker_stats\x18\x01 \x03(\x0b\x32\x32.taskqueue.GetWorkerStatsResponse.WorkerStatsEntry\x1aJ\n\x10WorkerStatsEntry\x12\x0b\n\x03key\x18\x01 \x01(\r\x12%\n\x05value\x18\x02 \x01(\x0b\x32\x16.taskqueue.WorkerStats:\x02\x38\x01\"\x1f\n\x10\x46\x65tchListRequest\x12\x0b\n\x03uri\x18\x01 \x01(\t\"\"\n\x11\x46\x65tchListResponse\x12\r\n\x05\x66iles\x18\x01 \x03(\t\"\x86\x01\n\x15UploadTemplateRequest\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x0f\n\x07version\x18\x02 \x01(\t\x12\x13\n\x0b\x64\x65scription\x18\x03 \x01(\t\x12\x0e\n\x06script\x18\x04 \x01(\x0c\x12\x1a\n\x12params_schema_json\x18\x05 \x01(\t\x12\r\n\x05\x66orce\x18\x06 \x01(\x08\"\x9e\x01\n\x16UploadTemplateResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\x12\x0f\n\x07message\x18\x02 \x01(\t\x12\x1c\n\x14workflow_template_id\x18\x03 \x01(\r\x12\x0c\n\x04name\x18\x04 \x01(\t\x12\x0f\n\x07version\x18\x05 \x01(\t\x12\x13\n\x0b\x64\x65scription\x18\x06 \x01(\t\x12\x10\n\x08warnings\x18\x07 \x01(\t\"M\n\x12RunTemplateRequest\x12\x1c\n\x14workflow_template_id\x18\x01 \x01(\r\x12\x19\n\x11param_values_json\x18\x02 \x01(\t\"\x9b\x01\n\x08Template\x12\x1c\n\x14workflow_template_id\x18\x01 \x01(\r\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\x0f\n\x07version\x18\x03 \x01(\t\x12\x13\n\x0b\x64\x65scription\x18\x04 \x01(\t\x12\x13\n\x0buploaded_at\x18\x05 \x01(\t\x12\x18\n\x0buploaded_by\x18\x06 \x01(\rH\x00\x88\x01\x01\x42\x0e\n\x0c_uploaded_by\"6\n\x0cTemplateList\x12&\n\ttemplates\x18\x01 \x03(\x0b\x32\x13.taskqueue.Template\"\xcb\x01\n\x0bTemplateRun\x12\x17\n\x0ftemplate_run_id\x18\x01 \x01(\r\x12\x1c\n\x14workflow_template_id\x18\x02 \x01(\r\x12\x18\n\x0bworkflow_id\x18\x03 \x01(\rH\x00\x88\x01\x01\x12\x12\n\ncreated_at\x18\x04 \x01(\t\x12\x19\n\x11param_values_json\x18\x05 \x01(\t\x12\x1a\n\rerror_message\x18\x06 \x01(\tH\x01\x88\x01\x01\x42\x0e\n\x0c_workflow_idB\x10\n\x0e_error_message\"7\n\x0fTemplateRunList\x12$\n\x04runs\x18\x01 \x03(\x0b\x32\x16.taskqueue.TemplateRun\"O\n\x11TemplateRunFilter\x12!\n\x14workflow_template_id\x18\x01 \x01(\rH\x00\x88\x01\x01\x42\x17\n\x15_workflow_template_id\"\x8b\x01\n\x18UpdateTemplateRunRequest\x12\x17\n\x0ftemplate_run_id\x18\x01 \x01(\r\x12\x18\n\x0bworkflow_id\x18\x02 \x01(\rH\x00\x88\x01\x01\x12\x1a\n\rerror_message\x18\x03 \x01(\tH\x01\x88\x01\x01\x42\x0e\n\x0c_workflow_idB\x10\n\x0e_error_message\"8\n\x14WorkspaceRootRequest\x12\x10\n\x08provider\x18\x01 \x01(\t\x12\x0e\n\x06region\x18\x02 \x01(\t\")\n\x15WorkspaceRootResponse\x12\x10\n\x08root_uri\x18\x01 \x01(\t2\x84\x17\n\tTaskQueue\x12=\n\nSubmitTask\x12\x16.taskqueue.TaskRequest\x1a\x17.taskqueue.TaskResponse\x12<\n\x0eRegisterWorker\x12\x15.taskqueue.WorkerInfo\x1a\x13.taskqueue.WorkerId\x12X\n\x13PingAndTakeNewTasks\x12$.taskqueue.PingAndGetNewTasksRequest\x1a\x1b.taskqueue.TaskListAndOther\x12?\n\x10UpdateTaskStatus\x12\x1b.taskqueue.TaskStatusUpdate\x1a\x0e.taskqueue.Ack\x12\x34\n\x0cSendTaskLogs\x12\x12.taskqueue.TaskLog\x1a\x0e.taskqueue.Ack(\x01\x12?\n\x14StreamTaskLogsOutput\x12\x11.taskqueue.TaskId\x1a\x12.taskqueue.TaskLog0\x01\x12<\n\x11StreamTaskLogsErr\x12\x11.taskqueue.TaskId\x1a\x12.taskqueue.TaskLog0\x01\x12\x42\n\x0cGetLogsChunk\x12\x19.taskqueue.GetLogsRequest\x1a\x17.taskqueue.LogChunkList\x12=\n\tListTasks\x12\x1b.taskqueue.ListTasksRequest\x1a\x13.taskqueue.TaskList\x12\x44\n\x0bListWorkers\x12\x1d.taskqueue.ListWorkersRequest\x1a\x16.taskqueue.WorkersList\x12>\n\x0c\x43reateWorker\x12\x18.taskqueue.WorkerRequest\x1a\x14.taskqueue.WorkerIds\x12=\n\x12UpdateWorkerStatus\x12\x17.taskqueue.WorkerStatus\x1a\x0e.taskqueue.Ack\x12\x35\n\x0c\x44\x65leteWorker\x12\x13.taskqueue.WorkerId\x1a\x10.taskqueue.JobId\x12>\n\x0cUpdateWorker\x12\x1e.taskqueue.WorkerUpdateRequest\x1a\x0e.taskqueue.Ack\x12T\n\x11GetWorkerStatuses\x12\x1e.taskqueue.WorkerStatusRequest\x1a\x1f.taskqueue.WorkerStatusResponse\x12;\n\x08ListJobs\x12\x1a.taskqueue.ListJobsRequest\x1a\x13.taskqueue.JobsList\x12K\n\x0eGetJobStatuses\x12\x1b.taskqueue.JobStatusRequest\x1a\x1c.taskqueue.JobStatusResponse\x12-\n\tDeleteJob\x12\x10.taskqueue.JobId\x1a\x0e.taskqueue.Ack\x12\x44\n\x0bListFlavors\x12\x1d.taskqueue.ListFlavorsRequest\x1a\x16.taskqueue.FlavorsList\x12\x42\n\x0fGetRcloneConfig\x12\x16.google.protobuf.Empty\x1a\x17.taskqueue.RcloneConfig\x12:\n\x05Login\x12\x17.taskqueue.LoginRequest\x1a\x18.taskqueue.LoginResponse\x12*\n\x06Logout\x12\x10.taskqueue.Token\x1a\x0e.taskqueue.Ack\x12=\n\nCreateUser\x12\x1c.taskqueue.CreateUserRequest\x1a\x11.taskqueue.UserId\x12\x39\n\tListUsers\x12\x16.google.protobuf.Empty\x1a\x14.taskqueue.UsersList\x12/\n\nDeleteUser\x12\x11.taskqueue.UserId\x1a\x0e.taskqueue.Ack\x12-\n\nUpdateUser\x12\x0f.taskqueue.User\x1a\x0e.taskqueue.Ack\x12\x42\n\x0e\x43hangePassword\x12 .taskqueue.ChangePasswordRequest\x1a\x0e.taskqueue.Ack\x12\x46\n\x0eListRecruiters\x12\x1a.taskqueue.RecruiterFilter\x1a\x18.taskqueue.RecruiterList\x12\x37\n\x0f\x43reateRecruiter\x12\x14.taskqueue.Recruiter\x1a\x0e.taskqueue.Ack\x12=\n\x0fUpdateRecruiter\x12\x1a.taskqueue.RecruiterUpdate\x1a\x0e.taskqueue.Ack\x12\x39\n\x0f\x44\x65leteRecruiter\x12\x16.taskqueue.RecruiterId\x1a\x0e.taskqueue.Ack\x12\x43\n\rListWorkflows\x12\x19.taskqueue.WorkflowFilter\x1a\x17.taskqueue.WorkflowList\x12\x43\n\x0e\x43reateWorkflow\x12\x1a.taskqueue.WorkflowRequest\x1a\x15.taskqueue.WorkflowId\x12\x37\n\x0e\x44\x65leteWorkflow\x12\x15.taskqueue.WorkflowId\x1a\x0e.taskqueue.Ack\x12\x37\n\tListSteps\x12\x15.taskqueue.WorkflowId\x1a\x13.taskqueue.StepList\x12\x37\n\nCreateStep\x12\x16.taskqueue.StepRequest\x1a\x11.taskqueue.StepId\x12/\n\nDeleteStep\x12\x11.taskqueue.StepId\x1a\x0e.taskqueue.Ack\x12U\n\x0eGetWorkerStats\x12 .taskqueue.GetWorkerStatsRequest\x1a!.taskqueue.GetWorkerStatsResponse\x12\x46\n\tFetchList\x12\x1b.taskqueue.FetchListRequest\x1a\x1c.taskqueue.FetchListResponse\x12U\n\x0eUploadTemplate\x12 .taskqueue.UploadTemplateRequest\x1a!.taskqueue.UploadTemplateResponse\x12\x44\n\x0bRunTemplate\x12\x1d.taskqueue.RunTemplateRequest\x1a\x16.taskqueue.TemplateRun\x12@\n\rListTemplates\x12\x16.google.protobuf.Empty\x1a\x17.taskqueue.TemplateList\x12L\n\x10ListTemplateRuns\x12\x1c.taskqueue.TemplateRunFilter\x1a\x1a.taskqueue.TemplateRunList\x12H\n\x11UpdateTemplateRun\x12#.taskqueue.UpdateTemplateRunRequest\x1a\x0e.taskqueue.Ack\x12U\n\x10GetWorkspaceRoot\x12\x1f.taskqueue.WorkspaceRootRequest\x1a .taskqueue.WorkspaceRootResponseB\x11Z\x0fgen/taskqueuepbb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'taskqueue_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  _globals['DESCRIPTOR']._loaded_options = None
  _globals['DESCRIPTOR']._serialized_options = b'Z\017gen/taskqueuepb'
  _globals['_TASKUPDATELIST_UPDATESENTRY']._loaded_options = None
  _globals['_TASKUPDATELIST_UPDATESENTRY']._serialized_options = b'8\001'
  _globals['_GETWORKERSTATSRESPONSE_WORKERSTATSENTRY']._loaded_options = None
  _globals['_GETWORKERSTATSRESPONSE_WORKERSTATSENTRY']._serialized_options = b'8\001'
  _globals['_TASKRESPONSE']._serialized_start=59
  _globals['_TASKRESPONSE']._serialized_end=90
  _globals['_WORKERINFO']._serialized_start=92
  _globals['_WORKERINFO']._serialized_end=160
  _globals['_TASKREQUEST']._serialized_start=163
  _globals['_TASKREQUEST']._serialized_end=725
  _globals['_TASK']._serialized_start=728
  _globals['_TASK']._serialized_end=1360
  _globals['_TASKLIST']._serialized_start=1362
  _globals['_TASKLIST']._serialized_end=1404
  _globals['_WORKER']._serialized_start=1407
  _globals['_WORKER']._serialized_end=1581
  _globals['_WORKERSLIST']._serialized_start=1583
  _globals['_WORKERSLIST']._serialized_end=1632
  _globals['_LISTWORKERSREQUEST']._serialized_start=1634
  _globals['_LISTWORKERSREQUEST']._serialized_end=1654
  _globals['_TASKUPDATE']._serialized_start=1656
  _globals['_TASKUPDATE']._serialized_end=1684
  _globals['_TASKUPDATELIST']._serialized_start=1687
  _globals['_TASKUPDATELIST']._serialized_end=1831
  _globals['_TASKUPDATELIST_UPDATESENTRY']._serialized_start=1762
  _globals['_TASKUPDATELIST_UPDATESENTRY']._serialized_end=1831
  _globals['_TASKLISTANDOTHER']._serialized_start=1834
  _globals['_TASKLISTANDOTHER']._serialized_end=1971
  _globals['_TASKSTATUSUPDATE']._serialized_start=1973
  _globals['_TASKSTATUSUPDATE']._serialized_end=2028
  _globals['_TASKLOG']._serialized_start=2030
  _globals['_TASKLOG']._serialized_end=2092
  _globals['_GETLOGSREQUEST']._serialized_start=2095
  _globals['_GETLOGSREQUEST']._serialized_end=2225
  _globals['_LOGCHUNK']._serialized_start=2227
  _globals['_LOGCHUNK']._serialized_end=2285
  _globals['_LOGCHUNKLIST']._serialized_start=2287
  _globals['_LOGCHUNKLIST']._serialized_end=2336
  _globals['_TASKIDS']._serialized_start=2338
  _globals['_TASKIDS']._serialized_end=2365
  _globals['_TASKID']._serialized_start=2367
  _globals['_TASKID']._serialized_end=2392
  _globals['_WORKERID']._serialized_start=2394
  _globals['_WORKERID']._serialized_end=2423
  _globals['_WORKERSTATUSREQUEST']._serialized_start=2425
  _globals['_WORKERSTATUSREQUEST']._serialized_end=2466
  _globals['_WORKERSTATUS']._serialized_start=2468
  _globals['_WORKERSTATUS']._serialized_end=2517
  _globals['_WORKERSTATUSRESPONSE']._serialized_start=2519
  _globals['_WORKERSTATUSRESPONSE']._serialized_end=2584
  _globals['_WORKERDETAILS']._serialized_start=2586
  _globals['_WORKERDETAILS']._serialized_end=2657
  _globals['_WORKERIDS']._serialized_start=2659
  _globals['_WORKERIDS']._serialized_end=2721
  _globals['_PINGANDGETNEWTASKSREQUEST']._serialized_start=2723
  _globals['_PINGANDGETNEWTASKSREQUEST']._serialized_end=2808
  _globals['_ACK']._serialized_start=2810
  _globals['_ACK']._serialized_end=2832
  _globals['_LISTTASKSREQUEST']._serialized_start=2834
  _globals['_LISTTASKSREQUEST']._serialized_end=2950
  _globals['_WORKERREQUEST']._serialized_start=2953
  _globals['_WORKERREQUEST']._serialized_end=3116
  _globals['_WORKERUPDATEREQUEST']._serialized_start=3119
  _globals['_WORKERUPDATEREQUEST']._serialized_end=3389
  _globals['_LISTFLAVORSREQUEST']._serialized_start=3391
  _globals['_LISTFLAVORSREQUEST']._serialized_end=3442
  _globals['_FLAVOR']._serialized_start=3445
  _globals['_FLAVOR']._serialized_end=3729
  _globals['_FLAVORSLIST']._serialized_start=3731
  _globals['_FLAVORSLIST']._serialized_end=3780
  _globals['_LISTJOBSREQUEST']._serialized_start=3782
  _globals['_LISTJOBSREQUEST']._serialized_end=3799
  _globals['_JOB']._serialized_start=3802
  _globals['_JOB']._serialized_end=3983
  _globals['_JOBID']._serialized_start=3985
  _globals['_JOBID']._serialized_end=4008
  _globals['_JOBSLIST']._serialized_start=4010
  _globals['_JOBSLIST']._serialized_end=4050
  _globals['_JOBSTATUSREQUEST']._serialized_start=4052
  _globals['_JOBSTATUSREQUEST']._serialized_end=4087
  _globals['_JOBSTATUS']._serialized_start=4089
  _globals['_JOBSTATUS']._serialized_end=4153
  _globals['_JOBSTATUSRESPONSE']._serialized_start=4155
  _globals['_JOBSTATUSRESPONSE']._serialized_end=4214
  _globals['_RCLONECONFIG']._serialized_start=4216
  _globals['_RCLONECONFIG']._serialized_end=4246
  _globals['_LOGINREQUEST']._serialized_start=4248
  _globals['_LOGINREQUEST']._serialized_end=4298
  _globals['_LOGINRESPONSE']._serialized_start=4300
  _globals['_LOGINRESPONSE']._serialized_end=4330
  _globals['_TOKEN']._serialized_start=4332
  _globals['_TOKEN']._serialized_end=4354
  _globals['_CREATEUSERREQUEST']._serialized_start=4356
  _globals['_CREATEUSERREQUEST']._serialized_end=4444
  _globals['_USERID']._serialized_start=4446
  _globals['_USERID']._serialized_end=4471
  _globals['_USER']._serialized_start=4473
  _globals['_USER']._serialized_end=4598
  _globals['_USERSLIST']._serialized_start=4600
  _globals['_USERSLIST']._serialized_end=4643
  _globals['_CHANGEPASSWORDREQUEST']._serialized_start=4645
  _globals['_CHANGEPASSWORDREQUEST']._serialized_end=4730
  _globals['_RECRUITERFILTER']._serialized_start=4732
  _globals['_RECRUITERFILTER']._serialized_end=4783
  _globals['_RECRUITERID']._serialized_start=4785
  _globals['_RECRUITERID']._serialized_end=4829
  _globals['_RECRUITER']._serialized_start=4832
  _globals['_RECRUITER']._serialized_end=5009
  _globals['_RECRUITERUPDATE']._serialized_start=5012
  _globals['_RECRUITERUPDATE']._serialized_end=5288
  _globals['_RECRUITERLIST']._serialized_start=5290
  _globals['_RECRUITERLIST']._serialized_end=5347
  _globals['_WORKFLOWFILTER']._serialized_start=5349
  _globals['_WORKFLOWFILTER']._serialized_end=5403
  _globals['_WORKFLOWID']._serialized_start=5405
  _globals['_WORKFLOWID']._serialized_end=5438
  _globals['_WORKFLOW']._serialized_start=5440
  _globals['_WORKFLOW']._serialized_end=5557
  _globals['_WORKFLOWREQUEST']._serialized_start=5559
  _globals['_WORKFLOWREQUEST']._serialized_end=5684
  _globals['_WORKFLOWLIST']._serialized_start=5686
  _globals['_WORKFLOWLIST']._serialized_end=5740
  _globals['_STEPID']._serialized_start=5742
  _globals['_STEPID']._serialized_end=5767
  _globals['_STEP']._serialized_start=5769
  _globals['_STEP']._serialized_end=5850
  _globals['_STEPREQUEST']._serialized_start=5852
  _globals['_STEPREQUEST']._serialized_end=5967
  _globals['_STEPLIST']._serialized_start=5969
  _globals['_STEPLIST']._serialized_end=6011
  _globals['_WORKERSTATS']._serialized_start=6014
  _globals['_WORKERSTATS']._serialized_end=6241
  _globals['_DISKUSAGE']._serialized_start=6243
  _globals['_DISKUSAGE']._serialized_end=6298
  _globals['_DISKIOSTATS']._serialized_start=6300
  _globals['_DISKIOSTATS']._serialized_end=6417
  _globals['_NETIOSTATS']._serialized_start=6419
  _globals['_NETIOSTATS']._serialized_end=6533
  _globals['_GETWORKERSTATSREQUEST']._serialized_start=6535
  _globals['_GETWORKERSTATSREQUEST']._serialized_end=6578
  _globals['_GETWORKERSTATSRESPONSE']._serialized_start=6581
  _globals['_GETWORKERSTATSRESPONSE']._serialized_end=6755
  _globals['_GETWORKERSTATSRESPONSE_WORKERSTATSENTRY']._serialized_start=6681
  _globals['_GETWORKERSTATSRESPONSE_WORKERSTATSENTRY']._serialized_end=6755
  _globals['_FETCHLISTREQUEST']._serialized_start=6757
  _globals['_FETCHLISTREQUEST']._serialized_end=6788
  _globals['_FETCHLISTRESPONSE']._serialized_start=6790
  _globals['_FETCHLISTRESPONSE']._serialized_end=6824
  _globals['_UPLOADTEMPLATEREQUEST']._serialized_start=6827
  _globals['_UPLOADTEMPLATEREQUEST']._serialized_end=6961
  _globals['_UPLOADTEMPLATERESPONSE']._serialized_start=6964
  _globals['_UPLOADTEMPLATERESPONSE']._serialized_end=7122
  _globals['_RUNTEMPLATEREQUEST']._serialized_start=7124
  _globals['_RUNTEMPLATEREQUEST']._serialized_end=7201
  _globals['_TEMPLATE']._serialized_start=7204
  _globals['_TEMPLATE']._serialized_end=7359
  _globals['_TEMPLATELIST']._serialized_start=7361
  _globals['_TEMPLATELIST']._serialized_end=7415
  _globals['_TEMPLATERUN']._serialized_start=7418
  _globals['_TEMPLATERUN']._serialized_end=7621
  _globals['_TEMPLATERUNLIST']._serialized_start=7623
  _globals['_TEMPLATERUNLIST']._serialized_end=7678
  _globals['_TEMPLATERUNFILTER']._serialized_start=7680
  _globals['_TEMPLATERUNFILTER']._serialized_end=7759
  _globals['_UPDATETEMPLATERUNREQUEST']._serialized_start=7762
  _globals['_UPDATETEMPLATERUNREQUEST']._serialized_end=7901
  _globals['_WORKSPACEROOTREQUEST']._serialized_start=7903
  _globals['_WORKSPACEROOTREQUEST']._serialized_end=7959
  _globals['_WORKSPACEROOTRESPONSE']._serialized_start=7961
  _globals['_WORKSPACEROOTRESPONSE']._serialized_end=8002
  _globals['_TASKQUEUE']._serialized_start=8005
  _globals['_TASKQUEUE']._serialized_end=10953
# @@protoc_insertion_point(module_scope)
