import React from 'react';

import {
    Table, Input, Button, Icon,
} from 'antd';

class MyTable extends React.Component {
    constructor(props) {
        super(props);
        this.url = props.url;
        this.state = {}
    }

    componentDidMount() {
        var self = this;
        fetch(this.url, {
            method: 'GET'
        }).then((response) => {
            return response.json();
        }).then((data) => {
            self.setState({
                dataSource: data.dataSource,
                columns: data.columns
            });
            console.log(data);
        })
    }

    sorter(a, b) {
        var stringA = a.name.toUpperCase(); // ignore upper and lowercase
        var stringB = b.name.toUpperCase(); // ignore upper and lowercase
        if (stringA < stringB) {
            return -1;
        }
        if (stringA > stringB) {
            return 1;
        }
        // names must be equal
        return 0;
    }

    setSorter(columns) {
        var self = this;
        if (columns) {
            columns = columns.map(function (column) {
                column.sorter = self.sorter;
                return column;
            });
        }
    }

    state = {
        searchText: '',
    };

    getColumnSearchProps = (dataIndex) => ({
        filterDropdown: ({
            setSelectedKeys, selectedKeys, confirm, clearFilters,
        }) => (
                <div className="custom-filter-dropdown">
                    <Input
                        ref={node => { this.searchInput = node; }}
                        placeholder={`Search ${dataIndex}`}
                        value={selectedKeys[0]}
                        onChange={e => setSelectedKeys(e.target.value ? [e.target.value] : [])}
                        onPressEnter={() => this.handleSearch(selectedKeys, confirm)}
                        style={{ width: 188, marginBottom: 8, display: 'block' }}
                    />
                    <Button
                        type="primary"
                        onClick={() => this.handleSearch(selectedKeys, confirm)}
                        icon="search"
                        size="small"
                        style={{ width: 90, marginRight: 8 }}
                    >
                        Search
                            </Button>
                    <Button
                        onClick={() => this.handleReset(clearFilters)}
                        size="small"
                        style={{ width: 90 }}
                    >
                        Reset
                            </Button>
                </div>
            ),
        filterIcon: filtered => <Icon type="search" style={{ color: filtered ? '#1890ff' : undefined }} />,
        onFilter: (value, record) => record[dataIndex].toString().toLowerCase().includes(value.toLowerCase()),
        onFilterDropdownVisibleChange: (visible) => {
            if (visible) {
                setTimeout(() => this.searchInput.select());
            }
        }
    })

    handleSearch = (selectedKeys, confirm) => {
        confirm();
        this.setState({ searchText: selectedKeys[0] });
    }

    handleReset = (clearFilters) => {
        clearFilters();
        this.setState({ searchText: '' });
    }

    setSearch(columns) {
        var self = this;

        if (columns) {
            columns = columns.map(function (column) {
                var map = self.getColumnSearchProps(column.key);
                for (var key in map) {
                    column[key] = map[key];
                }
                return column;
            });
        }
    }
    render() {
        var self = this;
        var dataSource = this.state.dataSource;
        var columns = this.state.columns;
        self.setSorter(columns);
        self.setSearch(columns);
        return <Table dataSource={dataSource} columns={columns} />;
    }
}

export { MyTable };