    import { writable, derived } from 'svelte/store';
    import { apiRequest } from '$lib/api';

    type Scholarship = {
        id: string;
        name: string;
        status: string;
        start_date: string;
        end_date: string;
        description: string;
        source: string;
        destination: string;
        target_audience: string;
        quota: string;
        unit_names: string[];
    };

    type Filters = {
        status: string[];
        unit_names: string[];
        sumber: string[];
        tujuan: string[];
        target: string[];
        quota: string[];
    };

    export const scholarships = writable<Scholarship[]>([]);
    export const filters = writable<Filters>({
        status: [],
        unit_names: [],
        sumber: [],
        tujuan: [],
        target: [],
        quota: [],
    });

    export const filterOptions = {
        status: ['on-going', 'coming-soon', 'closed'],
        unit_names: ['unit1', 'unit2', 'unit3'],
        sumber: ['source1', 'source2'],
        tujuan: ['destination1', 'destination2'],
        target: ['target1', 'target2'],
        quota: ['below-50', '50-100', 'above-100']
    };

    export const searchKeyword = writable("");

    export const filteredScholarships = derived(
    [scholarships, searchKeyword, filters],
    ([$scholarships, $searchKeyword, $filters]) => {
        const keyword = $searchKeyword.toLowerCase().trim();

        return $scholarships.filter(scholarship => {
            const matchesKeyword = scholarship.name.toLowerCase().includes(keyword);
            const matchesQuota =
                !$filters.quota.length || 
                $filters.quota.some(filterQuota => {
                const quota = parseInt(scholarship.quota) || 0; 
                if (filterQuota === 'below-50') return quota < 50;
                if (filterQuota === '50-100') return quota >= 50 && quota <= 100;
                if (filterQuota === 'above-100') return quota > 100;
                return false; 
                });
            const matchesStatus =
                $filters.status.length === 0 ||
                $filters.status.includes(scholarship.status.toLowerCase());
            const matchesUnitNames =
                $filters.unit_names.length === 0 ||
                $filters.unit_names.some(unitName => scholarship.unit_names.includes(unitName));
            const matchesSumber =
                $filters.sumber.length === 0 ||
                $filters.sumber.includes(scholarship.source.toLowerCase());
            const matchesTujuan =
                $filters.tujuan.length === 0 ||
                $filters.tujuan.includes(scholarship.destination.toLowerCase());
            const matchesTarget =
                $filters.target.length === 0 ||
                $filters.target.includes(scholarship.target_audience.toLowerCase());

            return matchesKeyword && matchesQuota && matchesStatus && matchesUnitNames && matchesSumber && matchesTujuan && matchesTarget;
        });
    }
    );

    export const ongoingScholarships = derived(scholarships, ($scholarships) => {
    return $scholarships.filter(scholarship => scholarship.status.toLowerCase() === 'on-going');
    });

    export async function fetchScholarships() {
    try {
        const data = await apiRequest('/scholarship/');
        scholarships.set(data);
    } catch (error) {
        console.error('Error fetching scholarships:', error);
    }
    }

    export function formatFaculties(faculties: string[]): string {
        if (!faculties || faculties.length === 0) return "Tidak ada fakultas";
        return faculties.join(", ");
    }

    export function formatDescription(description: string) {
        if (!description) return '';
        return description.replace(/<br>/g, '.....').replace(/<\/?p>/g, '');
    }

    export function normalizeStatus(status: string) {
        if (!status) return '';
        return status
            .replace(/-/g, ' ')     
            .replace(/\s+/g, ' ')     
            .trim()                   
            .toLowerCase()            
            .replace(/\b\w/g, (c) => c.toUpperCase());
    }

    export function getStatusColor(status: string) {
        const normalizedStatus = normalizeStatus(status);
        if (normalizedStatus === 'On Going') {
            return '#28a745'; 
        } else if (normalizedStatus === 'Coming Soon') {
            return '#002e5c'; 
        } else if (normalizedStatus === 'Closed') {
            return '#dc3545'; 
        }
        return '#6c757d'; 
    }

    export function updateFilter(type: keyof Filters, value: string) {
    filters.update(currentFilters => {
        const filterList = currentFilters[type];
        if (filterList.includes(value)) {
        return { ...currentFilters, [type]: filterList.filter(item => item !== value) };
        } else {
        return { ...currentFilters, [type]: [...filterList, value] };
        }
    });
    }